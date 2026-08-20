import sys
import os
import argparse
import time
from pathlib import Path

from pyspark.sql.functions import col

####################################################
# Project Root
####################################################

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT / "spark"))

####################################################
# Imports
####################################################

from common.config_loader import load_config
from framework.metadata.entity_config_loader import load_entity_config
from framework.spark.spark_session import create_spark_session
from framework.logging.logger import get_logger

from framework.transformation.silver_builder import build_silver
from framework.persistence.persist_silver import persist_silver
from framework.pipeline.pipeline_context import PipelineContext

####################################################
# Constants
####################################################

PENDING_STATUS = "PENDING"


def main():

    ####################################################
    # Parse Arguments
    ####################################################

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--entity",
        required=True,
        help="Entity Name"
    )

    args = parser.parse_args()

    entity_name = args.entity

    ####################################################
    # Environment
    ####################################################

    env = os.getenv("ENV", "local")

    print(f"Environment : {env}")
    print(f"Replay Entity : {entity_name}")

    ####################################################
    # Config
    ####################################################

    env_config = load_config(env)

    entity_config = load_entity_config(entity_name)

    ####################################################
    # Logger
    ####################################################

    logger = get_logger(
        "Replay Job",
        env_config
    )

    ####################################################
    # Spark Session
    ####################################################

    spark = create_spark_session(
        app_name="Replay Job",
        env=env,
        logger=logger
    )

    logger.info("Spark Session Created")

    ####################################################
    # Tables
    ####################################################

    catalog_name = env_config["iceberg"]["catalog_name"]

    silver_table = (
        f"{catalog_name}.silver.{entity_name}"
    )

    dlq_table = (
        f"{catalog_name}.dlq.records"
    )

    ####################################################
    # Read Pending Records
    ####################################################

    logger.info("Reading Pending Replay Records")

    replay_df = (
        spark.read
            .table(dlq_table)
            .filter(col("entity_name") == entity_name)
            .filter(col("replay_status") == PENDING_STATUS)
            .dropDuplicates(["event_id"])
    )

    replay_count = replay_df.count()

    logger.info(f"Replay Records Found : {replay_count}")

    if replay_count == 0:
        logger.info("No Pending Replay Records Found.")
        spark.stop()
        return

    ####################################################
    # Build Silver
    ####################################################

    logger.info("Starting Replay Processing")

    

    validated_df = build_silver(
        replay_df,
        entity_config=entity_config,
        env_config=env_config,
        entity_name=entity_name,
        logger=logger,
        replay=True
    )

    ####################################################
    # Persist Silver
    ####################################################

    persist_silver(
        validated_df=validated_df,
        context=PipelineContext(
            entity_name=entity_name,
            batch_id=int(time.time()),
            layer="silver",
            silver_table=silver_table,
            dlq_table=dlq_table,
            execution_mode="REPLAY"
        ),
        logger=logger,
        replay=True
    )

    logger.info("Replay Completed Successfully")

    ####################################################
    # Stop Spark
    ####################################################

    spark.stop()

    logger.info("Spark Session Closed")


if __name__ == "__main__":
    main()