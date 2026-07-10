from pyspark.sql import DataFrame
from framework.validation.constants import TEMP_COLUMN_PREFIX
from framework.validation.utils import append_validation_error
from pyspark.sql.functions import col

RULE_NAME = "allowed_values"

def validate_allowed_values(
        df: DataFrame,
        entity_config: dict
)-> DataFrame:
    print("Executing Allowed values validations")
    """
    Validate the DataFrame for allowed values constraints based on the entity configuration.

    Args:
        df (DataFrame): The input DataFrame to validate.
        entity_config (dict): The configuration dictionary containing validation rules.

    Returns:
        DataFrame: The validated DataFrame with allowed values constraints applied.
    """
    # Implementation of the allowed values validation logic goes here
    for column, metadata in entity_config.get("columns", {}).items():
        allowed_values = metadata.get('allowed_values')
        print(allowed_values)
        if "allowed_values" not in metadata:
            continue
        
        
        df = append_validation_error(
            df = df,
            condition = (col(column).isNotNull() & (~col(column).isin(allowed_values))),
            rule=RULE_NAME,
            column=column,
            error_message = f"{column} contains invalid values. Allowed values: {allowed_values}"
        )

    return df   