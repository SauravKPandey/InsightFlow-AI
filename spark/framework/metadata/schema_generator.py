from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    LongType,
    IntegerType,
    DoubleType,
    BooleanType,
    DateType,
    TimestampType,
)
TYPE_MAPPING = {
    "string": StringType,
    "long": LongType,
    "integer": IntegerType,
    "double": DoubleType,
    "boolean": BooleanType,
    "date": DateType,
    "timestamp": TimestampType,
    }

def generate_schema(entity_config):    
    """
    Generate a schema based on the entity configuration.
    """
    fields = []
    for column_name, metadata in entity_config["columns"].items():
        source_format = metadata.get("source_format")
        data_type = metadata.get("datatype", "string").lower()
        if data_type not in TYPE_MAPPING:
            raise ValueError(f"Unsupported data type: {data_type} for column: {column_name}")
        if source_format == "epoch_micros":
            spark_data_type = LongType()
        elif source_format == "epoch_days":
            spark_data_type = IntegerType()
        elif source_format == "epoch_millis":
            spark_data_type = LongType()
        else:
            spark_data_type = TYPE_MAPPING.get(data_type)()

        nullable = metadata.get("nullable", True)
        fields.append(StructField(column_name, spark_data_type, nullable))
    return StructType(fields)