from pyspark.sql import DataFrame
from pyspark.sql.functions import col, date_add, from_unixtime, timestamp_micros, lit, to_date
from framework.validation.constants import TEMP_COLUMN_PREFIX

def normalize_section(df: DataFrame, metadata_dict: dict, logger=None):

    for column_name, metadata in metadata_dict.items():

        if "source_format" not in metadata:
            continue

        source_format = metadata["source_format"]
        raw_column = f"{TEMP_COLUMN_PREFIX}{column_name}"
        #Preserving original column value in a new column with __raw_ prefix to validate the original value in case of any transformation or normalization
        df = df.withColumn(raw_column, col(column_name))

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
            error_msg = f"Unsupported source format: {source_format} for column: {column_name}"
            if logger:
                logger.error(error_msg)
            raise ValueError(
                f"Unsupported source format: {source_format}"
            )

    return df

def normalize(mapped_df, entity_config, logger=None):

    print("Running Normalizer")

    mapped_df = normalize_section(
        mapped_df,
        entity_config["columns"],
        logger=logger
    )

    mapped_df = normalize_section(
        mapped_df,
        entity_config["system_columns"],
        logger=logger
    )

    logger.info("Normalizer Completed")

    return mapped_df

