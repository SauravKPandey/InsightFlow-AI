import sys
import os
from pathlib import Path
import argparse
print("Creating Spark Session...")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT / "spark"))

from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from common.config_loader import load_config
from framework.metadata.entity_config_loader import (load_entity_config)
from framework.spark.spark_session import create_spark_session
from framework.iceberg.schema_loader import load_platform_schema
from framework.iceberg.table_manager import (
    ensure_namespace_exists,
    create_table_if_not_exists,
    write_to_iceberg
)

def main():

    #get entity name and environment from command line arguments

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--entity",
        required=True,
        help="Entity Name"
    )
    args = parser.parse_args()
    entity_name = args.entity

    #Read environment variable for ENV, default to "local" if not set
    env = os.getenv("ENV", "local")
    print(f"Environment: {env}")

    print(f"Starting Bronze Stream for Entity: {entity_name}")

    

    #Load configuration for environment and entity
    env_config = load_config(env)
    entity_config = load_entity_config(entity_name)

    ##Read configuration values for Kafka, root folder for storage paths and checkpoint paths from the loaded configurations
    bootstrap_servers = env_config["kafka"]["bootstrap_servers"]
    topic = entity_config["source"]["topic"]
    bronze_root = env_config["storage"]["bronze_root_path"]
    checkpoint_path = f"{env_config['storage']['checkpoint_root_path']}/bronze/{entity_config['entity_name']}"
    #Bronze schema path
    bronze_schema_path = PROJECT_ROOT / "configs" / "framework" / "bronze_schema.yaml"
    

    #create the bronze path using the entity name from the entity configuration
    bronze_path = (
        f"{bronze_root}/"
        f"{entity_config['entity_name']}"
    )
    
    

    #create Spark Session
    spark = create_spark_session("Bronze Stream", env)

    print("Spark Session Created")
    '''
    #Test if spark is able to write to path in GCS
    spark.range(10).write.mode("overwrite").parquet(
    "gs://insightflowai-data-prod/test/"
    )
    '''
    bronze_schema = load_platform_schema(bronze_schema_path)
    catalog = env_config["iceberg"]["catalog_name"]
    bronze_table = f"{catalog}.bronze.{entity_name}"
    ensure_namespace_exists(
        spark,
        catalog,
        "bronze"
    )
    create_table_if_not_exists(
        spark,
        catalog,
        "bronze",
        entity_name,
        bronze_schema

    )

    

    #Read data from Kafka topic and write to Bronze layer in Parquet format
    df = (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", bootstrap_servers)
        .option("subscribe", topic)
        .option("startingOffsets", "earliest")
        .load()
    )
    print("Kafka Stream Created")

    df.printSchema()

    #write to Iceberg Bronze table
    query = (df.writeStream.foreachBatch(
        lambda batch_df, batch_id: write_to_iceberg(
            batch_df,
            batch_id,
            bronze_table,
            mode="append"
        )
    ).option("checkpointLocation", checkpoint_path)
    .start()
    )

    print("Bronze Streaming Query Started")
    query.awaitTermination()


if __name__ == "__main__":
    main()

