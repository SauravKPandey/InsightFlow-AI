"""
DLQ Iceberg Schema

The DLQ is a platform-wide operational table.

It stores the original Kafka event together with
pipeline metadata and replay metadata.

One validation failure generates one DLQ record.
"""

from pyspark.sql.types import (
    StructType,
    StructField,
    BinaryType,
    StringType,
    IntegerType,
    LongType,
    TimestampType
)


DLQ_SCHEMA = StructType([

    ###############################################################
    # Original Kafka Event
    ###############################################################

    StructField("key", StringType(), True),

    StructField("raw_payload", StringType(), True),

    StructField("topic", StringType(), False),

    StructField("partition", IntegerType(), False),

    StructField("offset", LongType(), False),

    StructField("event_id", StringType(), False),

    StructField("timestamp", TimestampType(), True),

    StructField("timestampType", StringType(), True),

    ###############################################################
    # Pipeline Metadata
    ###############################################################

    StructField("entity_name", StringType(), False),

    StructField("failed_layer", StringType(), False),

    StructField("batch_id", LongType(), False),

    ###############################################################
    # Error Metadata
    ###############################################################

    StructField("error_type", StringType(), False),

    StructField("error_code", StringType(), False),

    StructField("error_column", StringType(), True),

    StructField("error_message", StringType(), False),

    ###############################################################
    # Replay Metadata
    ###############################################################

    StructField("retry_count", IntegerType(), False),

    StructField("replay_status", StringType(), False),

    StructField("rejected_timestamp", TimestampType(), False),

    StructField("replay_timestamp", TimestampType(), True)

])