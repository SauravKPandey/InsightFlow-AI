from pyspark.sql import DataFrame
from pyspark.sql.functions import col, lit, size
from framework.validation.constants import VALIDATION_ERROR_SCHEMA
from pyspark.sql.functions import array, struct, when, array, array_union


def append_validation_error(df,condition, rule, column, error_message)-> DataFrame:
    """
    Append a validation error to the DataFrame.

    Args:
        df (DataFrame): The input DataFrame.
        rule (str): The validation rule that failed.
        column (str): The column name where the validation failed.
        error_message (str): The error message describing the validation failure.

    Returns:
        DataFrame: The DataFrame with the appended validation error.
    """
    

    error = array(
        struct(
            lit(rule).alias("rule"),
            lit(column).alias("column"),
            lit(error_message).alias("error_message")
        )
    )
    
    # Append the new error to the Validation_Error column
    df = df.withColumn(
        "Validation_Error",
        when(condition, when(col("Validation_Error").isNull(), error).otherwise(
                        array_union(col("Validation_Error"), error))).otherwise(
                            col("Validation_Error"))
                            )
    
    return df
