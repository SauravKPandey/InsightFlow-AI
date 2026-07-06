from pyspark.sql import DataFrame
from pyspark.sql.functions import col, date_add, from_unixtime, timestamp_micros, lit, to_date


def normalize_section(df: DataFrame, metadata_dict: dict):

    for column_name, metadata in metadata_dict.items():

        if "source_format" not in metadata:
            continue

        source_format = metadata["source_format"]

        if source_format == "epoch_micros":

            df = df.withColumn(
                column_name,
                timestamp_micros(col(column_name))
            )

        elif source_format == "epoch_millis":

            df = df.withColumn(
                column_name,
                from_unixtime(
                    col(column_name).cast("long") / 1000
                ).cast("timestamp")
            )

        elif source_format == "epoch_days":

            df = df.withColumn(
                column_name,
                date_add(
                    to_date(lit("1970-01-01")),
                    col(column_name)
                )
            )

        else:

            raise ValueError(
                f"Unsupported source format: {source_format}"
            )

    return df

def normalize(mapped_df, entity_config):

    print("Running Normalizer")

    mapped_df = normalize_section(
        mapped_df,
        entity_config["columns"]
    )

    mapped_df = normalize_section(
        mapped_df,
        entity_config["system_columns"]
    )

    print("Normalizer Completed")

    return mapped_df

