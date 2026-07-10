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
from framework.monitoring.summary import summarize
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


BRONZE_SCHEMA = StructType([
    StructField("key", BinaryType(), True),
    StructField("value", BinaryType(), True),
    StructField("topic", StringType(), False),
    StructField("partition", IntegerType(), False),
    StructField("offset", LongType(), False),
    StructField("timestamp", TimestampType(), True),
    StructField("timestampType", StringType(), True)
])

def process_batch(
    batch_df,
    batch_id,
    entity_name,
    silver_table,
    logger
    ):

    valid_df = batch_df.filter((batch_df.Validation_Error.isNull() ) | (size(batch_df.Validation_Error) == 0)    )
    invalid_df = batch_df.filter(size(batch_df.Validation_Error) > 0)


    metrics = summarize(
        valid_df=valid_df,
        invalid_df=invalid_df,
        entity_name=entity_name,
        batch_id=batch_id
    )

    # TODO
    # write_to_dlq(...)

    # TODO
    # send_alert(...)

    valid_df = valid_df.drop(
        "Validation_Error"
    )

    write_to_iceberg(
        batch_df=valid_df,
        batch_id=batch_id,
        table_name=silver_table,
        mode="append",
        logger=logger
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

    ##Read environment variable for ENV, default to "local" if not set
    env = os.getenv("ENV", "local")
    print(f"Environment: {env}")

    print(f"Starting Silver Stream for Entity: {entity_name}")

    #Load configuration for environment and entity
    env_config = load_config(env)
    entity_config = load_entity_config(entity_name)

    #configure logging
    logger = get_logger(
    "silver_Stream",
    env_config
    )
    #silver schema path
    silver_schema_path = PROJECT_ROOT / "configs" / "entities" / f"{entity_name}.yaml"

    #create the bronze table and silver table names using the entity name from the entity configuration
    catalog_name = env_config['iceberg']['catalog_name']
    bronze_table = f"{catalog_name}.bronze.{entity_config['entity_name']}"
    logger.info(f"Bronze Table: {bronze_table}")

    silver_table = f"{catalog_name}.silver.{entity_config['entity_name']}"
    logger.info(f"Silver Table: {silver_table}")
    
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

    #create the silver table in the iceberg catalog if it does not exist, using the silver schema and the silver path
    create_table_if_not_exists(
    spark=spark,
    catalog=catalog_name,
    namespace="silver",
    table_name=entity_name,
    schema=silver_schema,
    logger=logger
    )

    #Read Bronze data from the bronze storage path in parquet format and convert to string format for Silver layer processing
    bronze_df = (
        spark.readStream
        .table(bronze_table)
    )
    logger.info("2. Bronze Stream Created")
    #call silver builder function to process the bronze data and and transform for silver layer processing and write to silver storage path in parquet format
    validated_df = build_silver(bronze_df, silver_schema, env_config, entity_name, logger=logger)
    logger.info("3. Silver DF Built")



    #print("Valid Rows")
    #valid_df.show()

    #print("Invalid Rows")
    #invalid_df.show(truncate=False)

    # Dropping not required cols
    validated_df = validated_df.drop(
    "topic",
    "partition",
    "offset",
    "timestamp",
)
    #write to silver storage path in parquet format with metadata and payload fields extracted from the bronze layer parquet data
    query = (
    validated_df.writeStream
      .foreachBatch(
            lambda batch_df, batch_id:
                process_batch(
                    batch_df=batch_df,
                    batch_id=batch_id,
                    entity_name=entity_name,
                    silver_table=silver_table,
                    logger = logger

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

if __name__ == "__main__":
    main()



