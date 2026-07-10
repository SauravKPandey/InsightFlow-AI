from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    ArrayType

)

VALIDATION_ERROR_SCHEMA = ArrayType(StructType([
    StructField("rule", StringType(), False),
    StructField("column", StringType(), False),
    StructField("error_message", StringType(), False)
])) 


TEMP_COLUMN_PREFIX = "__raw_"