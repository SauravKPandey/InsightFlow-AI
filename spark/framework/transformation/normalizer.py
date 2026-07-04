from pyspark.sql import DataFrame
from pyspark.sql.functions import col, date_add, from_unixtime, timestamp_micros, lit, to_date


def normalize(
        mapped_df: DataFrame,
        entity_config: dict
    ) -> DataFrame:
    print("Running Normalizer")
    """ Normalize the mapped DataFrame based on the entity configuration """

    for column_name, metadata in entity_config["columns"].items():
        print(entity_config["columns"].keys())
        print(f"Column: {column_name}")
        
        if "source_format" in metadata:
            source_format = metadata["source_format"]
            print(f"Source format: {repr(source_format)}")
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
            elif source_format == "epoch_millis":
                print(">>>> ENTERED epoch_millis <<<<")
                mapped_df = mapped_df.withColumn(
                    column_name,
                    from_unixtime(
            col(column_name).cast("long") / 1000
        ).cast("timestamp")
                )
            else:
                raise ValueError(f"Unsupported source format: {source_format} for column: {column_name}")
            
            
    print("Normalizer Completed")
    return mapped_df


