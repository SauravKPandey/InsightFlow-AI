"""
Validation Splitter

Splits the validated dataframe into
1. Valid Records
2. Invalid Records

A record is considered valid when Validation_Error is NULL
or an empty array.
"""

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, size
from framework.validation.constants import VALIDATION_ERROR_COLUMN

def split_valid_invalid(
    validated_df: DataFrame
) -> tuple[DataFrame, DataFrame]:
    """
    Split the validated dataframe into valid and invalid records.

    Args:
        validated_df:
            DataFrame returned by build_silver()

    Returns:
        (valid_df, invalid_df)
    """

    valid_df = validated_df.filter(
        col(VALIDATION_ERROR_COLUMN).isNull()
        | (size(col(VALIDATION_ERROR_COLUMN)) == 0)
    )

    invalid_df = validated_df.filter(
        col(VALIDATION_ERROR_COLUMN).isNotNull()
        & (size(col(VALIDATION_ERROR_COLUMN)) > 0)
    )

    return valid_df, invalid_df