#import relevant packages
import sys
import os
import argparse 
from pathlib import Path
from pyspark.sql import SparkSession    
from pyspark.sql.functions import col


#fetch the project root directory 
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT / "spark"))
#PROJECT_ROOT = Path.cwd()
#sys.path.append(str(PROJECT_ROOT / "spark"))
from framework.iceberg.schema_loader import load_platform_schema
#from framework.iceberg.iceberg_utils import (ensure_namespace_exists)
from framework.iceberg.table_manager import create_table_if_not_exists, ensure_namespace_exists, write_to_iceberg
from common.config_loader import load_config
from framework.metadata.entity_config_loader import (load_entity_config)
from framework.transformation.silver_builder import (build_silver)
from framework.iceberg.schema_adapter import struct_to_platform_schema

from pyspark.sql.types import (
    StructType,
    StructField,
    BinaryType,
    StringType,
    IntegerType,
    LongType,
    TimestampType
)
from framework.spark.spark_session import create_spark_session
from framework.logging.logger import get_logger
from pyspark.sql.functions import col, size
from framework.validation.splitter import split_valid_invalid
from framework.pipeline.pipeline_context import PipelineContext
from framework.persistence.persist_silver import persist_silver
from framework.dlq.dlq_schema import DLQ_SCHEMA


BRONZE_SCHEMA = StructType([
    StructField("key", StringType(), True),
    StructField("raw_payload", StringType(), True),
    StructField("topic", StringType(), False),
    StructField("partition", IntegerType(), False),
    StructField("offset", LongType(), False),
    StructField("timestamp", TimestampType(), True),
    StructField("timestampType", StringType(), True)
])

DLQ_PLATFORM_SCHEMA = struct_to_platform_schema(
    DLQ_SCHEMA
)

    

def main():

    

    #fetch the entity name and environment from command line arguments, default to "local" if not provided
    parser = argparse.ArgumentParser()
    parser.add_argument(
    "--entity",
    required=True,
    help="Entity Name"
    )
    args = parser.parse_args()
    entity_name = args.entity
    env = os.getenv("ENV", "local")
    print(f"Environment: {env}")
    #Load configuration for environment and entity
    env_config = load_config(env)
    entity_config = load_entity_config(entity_name)
    #configure logging
    logger = get_logger(
            "silver_Stream",
            env_config
            )
    
    
    print(f"Starting Silver Stream for Entity: {entity_name}")
    ##Read environment variable for ENV, default to "local" if not set
    try:
        

        

        
        #silver schema path
        silver_schema_path = PROJECT_ROOT / "configs" / "entities" / f"{entity_name}.yaml"

        #create the bronze table and silver table names using the entity name from the entity configuration
        catalog_name = env_config['iceberg']['catalog_name']
        bronze_table = f"{catalog_name}.bronze.{entity_config['entity_name']}"
        logger.info(f"Bronze Table: {bronze_table}")

        silver_table = f"{catalog_name}.silver.{entity_config['entity_name']}"
        logger.info(f"Silver Table: {silver_table}")

        dlq_table = f"{catalog_name}.dlq.records"
        
        #create a checkpoint path for the silver stream using the entity name from the entity configuration
        checkpoint_path = (
        f"{env_config['storage']['checkpoint_root_path']}/silver/{entity_config['entity_name']}"
        )
        logger.info(f"Checkpoint Path: {checkpoint_path}")        

        #create Spark Session
        spark = create_spark_session("Silver Stream", env,logger=logger)
            
        logger.info("1. Spark Session Created")

        #Crete bronze schema to allow spark to read the bronze parquet files and convert to string format for silver layer processing
        silver_schema = load_platform_schema(silver_schema_path, logger=logger)  

        #ensure the silver namespace exists in the iceberg catalog, if not create it
        ensure_namespace_exists(spark, catalog_name, "silver", logger=logger)

        #ensure tyyhe dlq namespace exists:
        ensure_namespace_exists(spark, catalog_name, "dlq", logger=logger)

        #create the silver table in the iceberg catalog if it does not exist, using the silver schema and the silver path
        create_table_if_not_exists(
        spark=spark,
        catalog=catalog_name,
        namespace="silver",
        table_name=entity_name,
        schema=silver_schema,
        logger=logger
        )

        create_table_if_not_exists(
        spark=spark,
        catalog=catalog_name,
        namespace="dlq",
        table_name="records",
        schema=DLQ_PLATFORM_SCHEMA,
        logger=logger
        )

        #Read Bronze data from the bronze storage path in parquet format and convert to string format for Silver layer processing
        bronze_df = (
            spark.readStream
            .table(bronze_table)
        )
        logger.info("2. Bronze Stream Created")

        #call silver builder function to process the bronze data and and transform for silver layer processing and write to silver storage path in parquet format
        validated_df = build_silver(bronze_df, silver_schema, env_config, entity_name, logger, False)
        logger.info("3. Silver DF Built")



        #print("Valid Rows")
        #valid_df.show()

        #print("Invalid Rows")
        #invalid_df.show(truncate=False)

    
        #write to silver storage path in parquet format with metadata and payload fields extracted from the bronze layer parquet data
        query = (
        validated_df.writeStream
        .foreachBatch(
                lambda batch_df, batch_id:
                    persist_silver(
                    validated_df=batch_df,
                    context=PipelineContext(
                        entity_name=entity_name,
                        batch_id=batch_id,
                        layer="silver",
                        silver_table=silver_table,
                        dlq_table = dlq_table,
                        execution_mode="LIVE"
                    ),
                    logger=logger
                )
        )

        .option(
            "checkpointLocation",
            checkpoint_path
        )
        .start()
    )
        logger.info("4. Stream Started")
        query.awaitTermination()

    except Exception as e:
        if logger:
            logger.error(
                f"[FATAL] Silver Streaming Pipeline failed for entity '{entity_name}': {str(e)}",
                exc_info=True
            )
        else:
            print(f"[FATAL ERROR] Pipeline startup failed before logger initialized: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()



