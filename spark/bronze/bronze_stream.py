import sys
import os
from pathlib import Path
import argparse
print("Creating Spark Session...")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from common.config_loader import load_config
from framework.metadata.entity_config_loader import (load_entity_config)

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
    checkpoint_path = env_config["checkpoint"]["root_path"]

    #create the bronze path using the entity name from the entity configuration
    bronze_path = (
        f"{bronze_root}/"
        f"{entity_config['entity_name']}"
    )
    
    #cretae checkpoint path using the entity name from the entity configuration
    checkpoint_path = (
        f"{checkpoint_path}/{bronze_path}" 
    )

    #create Spark Session
    spark = (
        SparkSession.builder
        .appName("BronzeStream")
        .getOrCreate() 
    )

    print("Spark Session Created")

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


    #Write to Bronze layer in Parquet format with append mode and checkpointing for fault tolerance
    query = (
        df.writeStream
        .format("parquet")
        .option("path", bronze_path)
        .outputMode("append")
        .option("checkpointLocation", checkpoint_path)
        .start()
    )

    print("Bronze Streaming Query Started")
    query.awaitTermination()

if __name__ == "__main__":
    main()

