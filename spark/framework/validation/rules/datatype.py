from pyspark.sql import DataFrame
from framework.validation.utils import append_validation_error
from pyspark.sql.functions import col
from framework.validation.constants import  TEMP_COLUMN_PREFIX
RULE_NAME = "datatype"

def validate_datatype(
        df: DataFrame,
        entity_config: dict
)-> DataFrame:
    """
    Validate the DataFrame based on the entity configuration.

    Args:
        df (DataFrame): The input DataFrame to validate.
        entity_config (dict): The configuration dictionary containing validation rules.

    Returns:
        DataFrame: The validated DataFrame with constraints applied.
    """
    # Implementation of the validation logic goes here
    # This is a placeholder for the actual validation code
     
    for column, rules in entity_config.get("columns", {}).items():
        
        if "source_format" not in rules:
            continue  # Skip columns without a specified type

        # Check if the column exists in the DataFrame
        if column not in df.columns:
            continue  # Skip columns that are not present in the DataFrame

        # Validate if the column transformation was successful and the column is not null
        raw_column = f"{TEMP_COLUMN_PREFIX}{column}"    
           
        df = append_validation_error(
                df,
                condition=col(column).isNotNull() & col(raw_column).isNull(),  # Only check non-null values for datatype validation
                rule=RULE_NAME,
                column=column,
                error_message=f"Failed to convert '{column}' from {rules['source_format']} to {rules['datatype']}. Please check the original value in '{raw_column}' column."
            )



    return df