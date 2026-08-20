from pyspark.sql.types import StructType


SPARK_TO_PLATFORM_TYPES = {
    "StringType": "string",
    "IntegerType": "integer",
    "LongType": "long",
    "TimestampType": "timestamp",
    "DateType": "date",
    "BinaryType": "binary",
    "BooleanType": "boolean",
    "DoubleType": "double",
    "FloatType": "float"
}


def struct_to_platform_schema(schema: StructType) -> dict:

    columns = {}

    for field in schema.fields:

        columns[field.name] = {
            "datatype": SPARK_TO_PLATFORM_TYPES[
                field.dataType.__class__.__name__
            ],
            "nullable": field.nullable
        }

    return {
        "columns": columns,
        "system_columns": {}
    }