
from pyspark.sql import DataFrame
from framework.validation.utils import append_validation_error
from pyspark.sql.functions import col
RULE_NAME = "not_null"
def validate_not_null(
        df: DataFrame,
        entity_config: dict
)-> DataFrame:
    """
    Validate the DataFrame for not null constraints based on the entity configuration.

    Args:
        df (DataFrame): The input DataFrame to validate.
        entity_config (dict): The configuration dictionary containing validation rules.

    Returns:
        DataFrame: The validated DataFrame with not null constraints applied.
    """
    # Implementation of the not null validation logic goes here
    for column, rules in entity_config.get("columns", {}).items():
        if rules.get("nullable", True):
            continue  # Skip columns that are allowed to be null
        df = append_validation_error(
            df,
            condition=col(column).isNull(),
            rule=RULE_NAME,   
            column=column,
            error_message=f"{column} cannot be null"
        )


    return df