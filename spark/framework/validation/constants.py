from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    ArrayType

)


"""
===========================================================
Validation
===========================================================
"""

TEMP_COLUMN_PREFIX = "__raw_"
VALIDATION_ERROR_COLUMN = "Validation_Error"
VALIDATION_ERROR_SCHEMA = ArrayType(StructType([
    StructField("rule", StringType(), False),
    StructField("column", StringType(), False),
    StructField("error_message", StringType(), False)
])) 

"""
===========================================================
Persistence
===========================================================
"""

SILVER_DROP_COLUMNS = [
    "topic",
    "partition",
    "offset",
    "timestamp",
    "key",
    "raw_payload",
    "timestampType",
    VALIDATION_ERROR_COLUMN
]

"""
===========================================================
DLQ
===========================================================
"""

FAILED_LAYER_SILVER = "silver"

ERROR_TYPE_VALIDATION = "VALIDATION"
ERROR_TYPE_PARSING = "PARSING"
ERROR_TYPE_MAPPING = "MAPPING"
ERROR_TYPE_SYSTEM = "SYSTEM"

REPLAY_PENDING = "PENDING"
REPLAY_IN_PROGRESS = "IN_PROGRESS"
REPLAY_SUCCESS = "SUCCESS"
REPLAY_FAILED = "FAILED"

INITIAL_RETRY_COUNT = 0

# ===========================================================
# DLQ Columns
# ===========================================================

DLQ_ERROR_CODE_COLUMN = "error_code"
DLQ_ERROR_MESSAGE_COLUMN = "error_message"
DLQ_ERROR_TYPE_COLUMN = "error_type"
DLQ_FAILED_LAYER_COLUMN = "failed_layer"
DLQ_ENTITY_NAME_COLUMN = "entity_name"
DLQ_RETRY_COUNT_COLUMN = "retry_count"
DLQ_REPLAY_STATUS_COLUMN = "replay_status"
DLQ_REJECTED_TIMESTAMP_COLUMN = "rejected_timestamp"
DLQ_REPLAY_TIMESTAMP_COLUMN = "replay_timestamp"

# ===========================================================
# Pipeline Layers
# ===========================================================

LAYER_BRONZE = "bronze"
LAYER_SILVER = "silver"
LAYER_CORE = "core"
LAYER_GOLD = "gold"

# ===========================================================
# Execution Modes
# ===========================================================

EXECUTION_MODE_LIVE = "LIVE"
EXECUTION_MODE_REPLAY = "REPLAY"