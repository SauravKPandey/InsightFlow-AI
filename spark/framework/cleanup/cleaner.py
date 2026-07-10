from pyspark.sql import DataFrame

from framework.validation.constants import TEMP_COLUMN_PREFIX


def cleanup(df: DataFrame) -> DataFrame:
    """
    Remove temporary framework columns before writing to Silver.
    """

    columns_to_drop = [
        column
        for column in df.columns
        if column.startswith(TEMP_COLUMN_PREFIX)
    ]

    if columns_to_drop:
        df = df.drop(*columns_to_drop)

    return df