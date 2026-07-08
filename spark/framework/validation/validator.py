
import array

from pyspark.sql import DataFrame
from pathlib import Path
import os
import sys
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType
)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT / "spark"))

from framework.validation.rules.allowed_values import validate_allowed_values
from framework.validation.rules.datatype import validate_datatype
from framework.validation.rules.not_null import validate_not_null
from framework.validation.constants import VALIDATION_ERROR_SCHEMA
from pyspark.sql.functions import lit, col, size

VALIDATORS = {
    validate_not_null,
    #validate_allowed_values,
    #validate_datatype
}
def validate(
        df: DataFrame,
        entity_config: dict
)-> tuple[DataFrame, DataFrame]:
    
    """
        Validate the DataFrame based on the entity configuration.

        Args:
            df (DataFrame): The input DataFrame to validate.
            entity_config (dict): The configuration dictionary containing validation rules.

        Returns:
            DataFrame: The validated DataFrame with constraints applied.
        """
        # Implementation of the validation logic goes here
        #1. Validate not null constraints
    df = df.withColumn("Validation_Error", lit(None).cast(VALIDATION_ERROR_SCHEMA))

    for validator in VALIDATORS:
        df = validator(df, entity_config)


    valid_df = df.filter((df.Validation_Error.isNull() ) | (size(df.Validation_Error) == 0)    )
    invalid_df = df.filter(size(df.Validation_Error) > 0)


        # This is a placeholder for the actual validation code
    return valid_df, invalid_df 
    

