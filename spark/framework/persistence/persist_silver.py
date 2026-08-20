from pyspark.sql import DataFrame
from pyspark.sql.functions import lit

from framework.pipeline.pipeline_context import PipelineContext
from framework.validation.constants import SILVER_DROP_COLUMNS, REPLAY_FAILED, REPLAY_SUCCESS
from framework.validation.splitter import split_valid_invalid
from framework.monitoring.summary import summarize
from framework.iceberg.table_manager import write_to_iceberg
from framework.dlq.dlq_writer import (build_dlq_dataframe , write_to_dlq)
from replay.replay_status_updater import update_replay_status



def persist_silver(
    validated_df: DataFrame,
    context: PipelineContext,
    logger,
    replay = False

):
    """
    Persist validated Silver dataframe.

    Responsibilities

    1. Split valid / invalid records
    2. Validation summary
    3. Write invalid records to DLQ (future)
    4. Drop operational metadata
    5. Write valid records to Silver
    """

    logger.info("Persisting Silver Batch")

    ####################################################
    # Split
    ####################################################

    valid_df, invalid_df = split_valid_invalid(
        validated_df
    )

    ####################################################
    # Summary
    ####################################################

    summarize(
        valid_df=valid_df,
        invalid_df=invalid_df,
        entity_name=context.entity_name,
        batch_id=context.batch_id,
        logger = logger
    )

    ####################################################
    # DLQ
    ####################################################

    #
    # Commit-4
    #
    if not replay:

        dlq_df = build_dlq_dataframe(
        invalid_df,
        context,
        logger
        )

        
        
        write_to_dlq(
        dlq_df=dlq_df,
        context=context,
        logger=logger
        )
    ####################################################
    # Drop Operational Columns
    ####################################################
    else :
        success_df = (
        valid_df
            .select("event_id")
            .distinct()
            .withColumn(
                "replay_status",
                lit(REPLAY_SUCCESS)
            )
            
        )

        failure_df = (
            invalid_df
                .select("event_id")
                .distinct()
                .withColumn(
                    "replay_status",
                    lit(REPLAY_FAILED)
                )
                
        )
        #update the dlq table status col "replay_status" as succesful using valid df
        update_replay_status(
            validated_df.sparkSession,
            success_df,
            context.dlq_table,
            logger
        )

        #update dlq table status col replay_status to "Failure" using invalid_df
        update_replay_status(
            validated_df.sparkSession,
            failure_df,
            context.dlq_table,
            logger
        )


        # Update replay metadata
        #
     
        logger.info("Replay mode - skipping DLQ insert")
    valid_df = valid_df.drop(
        *SILVER_DROP_COLUMNS,
        "event_id"
    )

    ####################################################
    # Write valid df to Silver
    ####################################################

    write_to_iceberg(
        batch_df=valid_df,
        batch_id=context.batch_id,
        table_name=context.silver_table,
        mode="append",
        logger=logger
    )

    logger.info("Silver Persistence Completed")

    