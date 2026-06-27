#import relevant packages
import sys
import os
import argparse 
from pathlib import Path
from pyspark.sql import SparkSession    
from pyspark.sql.functions import col
#fetch the project root directory 
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))
from common.config_loader import load_config
from framework.metadata.entity_config_loader import (load_entity_config)
from framework.transformation.silver_builder import (build_silver)
from pyspark.sql.types import (
    StructType,
    StructField,
    BinaryType,
    StringType,
    IntegerType,
    LongType,
    TimestampType
)


BRONZE_SCHEMA = StructType([
    StructField("key", BinaryType(), True),
    StructField("value", BinaryType(), True),
    StructField("topic", StringType(), False),
    StructField("partition", IntegerType(), False),
    StructField("offset", LongType(), False),
    StructField("timestamp", TimestampType(), True),
    StructField("timestampType", StringType(), True)
])


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

    print(f"Starting Bronze Stream for Entity: {entity_name}")

    #Load configuration for environment and entity
    env_config = load_config(env)
    entity_config = load_entity_config(entity_name)
    

    #fetch env configuration, bronze storage path for reading parquet, silver storage path for write from the config_loader.py file
    bronze_path = (f"{env_config['storage']['bronze_root_path']}/{entity_config['entity_name']}")
    silver_path = f"{env_config['storage']['silver_root_path']}/{entity_config['entity_name']}"
    
    checkpoint_path = f"{env_config['checkpoint']['root_path']}/{silver_path}"

    print(f"Bronze Path: {bronze_path}")
    print(f"Silver Path: {silver_path}")
    print(f"Checkpoint Path: {checkpoint_path}")        
    #fetch entity configuration from the entity_config_loader.py file

    #fetch schema from the entity configuration for the entity name provided in the command line argument

    #create Spark Session
    spark = (
        SparkSession.builder
        .appName("BronzeStream")
        .getOrCreate()
    )
    print("1. Spark Session Created")

    #Crete bronze schema to allow spark to read the bronze parquet files and convert to string format for silver layer processing
    

    #Read Bronze data from the bronze storage path in parquet format and convert to string format for Silver layer processing
    bronze_df = (
        spark.readStream
        .schema(BRONZE_SCHEMA)
        .format("parquet")
        .load(bronze_path)
        
    )
    print("2. Bronze Stream Created")
    #call silver builder function to process the bronze data and and transform for silver layer processing and write to silver storage path in parquet format
    silver_df = build_silver(bronze_df, entity_config, env_config, entity_name)
    print("3. Silver DF Built")
    
    #write to silver storage path in parquet format with metadata and payload fields extracted from the bronze layer parquet data
    querry = (
        silver_df.writeStream
        .outputMode("append")
        .format("parquet")
        .option("path", silver_path)
        .option("checkpointLocation", checkpoint_path)
        .start()
        
    )
    print("4. Stream Started")
    querry.awaitTermination()

if __name__ == "__main__":
    main()



