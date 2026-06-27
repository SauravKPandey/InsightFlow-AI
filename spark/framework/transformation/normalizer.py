from pyspark.sql import DataFrame
from pyspark.sql.functions import col, date_add, timestamp_micros, lit, to_date


def normalize(
        mapped_df: DataFrame,
        entity_config: dict
    ) -> DataFrame:

    """ Normalize the mapped DataFrame based on the entity configuration """

    for column_name, metadata in entity_config["columns"].items():
        if "source_format" in metadata:
            source_format = metadata["source_format"]
            if source_format == "epoch_micros":
                mapped_df = mapped_df.withColumn(
                    column_name,
                    timestamp_micros(col(column_name))
                )
            elif source_format == "epoch_days":
                mapped_df = mapped_df.withColumn(
                    column_name,
                    date_add(to_date(lit("1970-01-01")), col(column_name))

                )
            else:
                raise ValueError(f"Unsupported source format: {source_format} for column: {column_name}")
            
    return mapped_df


