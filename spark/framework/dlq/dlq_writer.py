from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    explode,
    col,
    lit,
    current_timestamp,
    concat_ws
)
from framework.iceberg.table_manager import write_to_iceberg

from framework.pipeline.pipeline_context import PipelineContext
from framework.validation.constants import (
    VALIDATION_ERROR_COLUMN,
    ERROR_TYPE_VALIDATION,
    REPLAY_PENDING,
    INITIAL_RETRY_COUNT
)

def write_to_dlq(
    dlq_df: DataFrame,
    context: PipelineContext,
    logger
):
    """
    Persist DLQ dataframe into Iceberg.
    """

    logger.info(
        f"Writing  validation failures to DLQ..."
    )

    write_to_iceberg(
        batch_df=dlq_df,
        batch_id=context.batch_id,
        table_name=context.dlq_table,
        mode="append",
        logger=logger
    )

    logger.info("DLQ write completed.")




def build_dlq_dataframe(
    invalid_df: DataFrame,
    context: PipelineContext,
    logger
) -> DataFrame:
    
    logger.info("Building DLQ DataFrame")
    
    """
    The fn will execute 5 things:
        invalid_df
        ↓
        explode Validation_Error
        ↓
        Extract
        rule
        column
        message
        ↓
        Add operational metadata
        ↓
        Write Iceberg
    """
    dlq_df = (
        invalid_df
        .withColumn(
    "event_id",
    concat_ws(
        ":",
        col("topic"),
        col("partition").cast("string"),
        col("offset").cast("string")
            )
        )

         # One validation error -> One DLQ record
        .withColumn(
            "validation_error",explode(col(VALIDATION_ERROR_COLUMN))
        )
        # operational metadata
        .withColumn(
            "entity_name", lit(context.entity_name)
        )
        .withColumn(
            "failed_layer",lit(context.layer)
        )
        .withColumn(
            "batch_id", lit(context.batch_id)
        )
        .withColumn(
            "error_type", lit(ERROR_TYPE_VALIDATION)
        )
        .withColumn(
            "retry_count", lit(INITIAL_RETRY_COUNT)
        )
        .withColumn(
            "replay_status", lit(REPLAY_PENDING)
        )
        .withColumn(
            "rejected_timestamp", current_timestamp()
        )
        .withColumn(
            "replay_timestamp", lit(None).cast("timestamp")
        )

        ####################################################
        # Final Schema
        ####################################################
        .select(

            # ---------- Original Kafka Event ----------
            "event_id",
            "key",
            "raw_payload",
            "topic",
            "partition",
            "offset",
            "timestamp",
            "timestampType",

            # ---------- Pipeline Metadata ----------

            "entity_name",
            "failed_layer",
            "batch_id",

            # ---------- Error Metadata ----------

            "error_type",

            col("validation_error.rule")
                .alias("error_code"),

            col("validation_error.column")
                .alias("error_column"),

            col("validation_error.error_message")
                .alias("error_message"),

            # ---------- Replay Metadata ----------

            "retry_count",
            "replay_status",
            "rejected_timestamp",
            "replay_timestamp"
        )
    )

    logger.info("DLQ DataFrame Built Successfully")

    


    return dlq_df

    