
import sys
from pathlib import Path
print("Creating Spark Session...")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from common.config_loader import load_config
from pyspark.sql.functions import from_json
from framework.metadata.entity_config_loader import (load_entity_config)
from framework.parser.debezium_parser import (parse_debezium)
from framework.mapper.entity_mapper import (map_entity)



def build_silver(bronze_df, entity_config, env_config, entity_name, logger=None):
    """
    Silver Builder function to read Bronze data, process it, and write to Silver layer.
    """
    if logger:
        logger.info("Starting Silver Builder...")
    else:
        print("Starting Silver Builder...")

    
    logger.info("Bronze Data Read Successfully from stream file")
    silver_write_path = env_config["storage"]["silver_root_path"] + f"/{entity_name}"
    logger.info(f"Silver Data will be written to: {silver_write_path}")

    #Read Parquet files from Bronze layer and convert to string format for Silver layer processing
    logger.info("Extracting Required Fields for Silver Layer Processing...")

    
    bronze_decoded_df = bronze_df.select(
        col("key").cast("string").alias("key"),
        col("value").cast("string").alias("raw_payload"),
        col("topic").alias("topic"),
        col("partition").alias("partition"),
        col("offset").alias("offset"),
        col("timestamp").alias("timestamp"),
        col("timestampType")
    )

    #get the parsed cdc df
    logger.info("calling parse_debezium function to extract before, after, op, source, ts_ms from raw_payload")
    cdc_df = parse_debezium(bronze_decoded_df, logger=logger)
    


    #call map_entity fn to convert cddc even into entity-specific silver records
    print("calling map_entity function to convert cdc event into entity-specific silver records")
    silver_df = map_entity(cdc_df, entity_config,logger=logger)

    #print("silver dataframe:", silver_df)

    return silver_df