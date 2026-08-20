from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from framework.logging.logger import get_logger

TYPE_MAPPING = {
    "string": "STRING",
    "integer": "INT",
    "long": "BIGINT",
    "timestamp": "TIMESTAMP",
    "date": "DATE",
    "binary": "BINARY",
    "boolean": "BOOLEAN",
    "double": "DOUBLE",
    "float": "FLOAT"
}

def ensure_namespace_exists(
        spark: SparkSession, 
        catalog: str,
        namespace: str,
        logger=None
):
    """
    Ensure that the specified namespace exists in the given catalog. If it does not exist, create it.

    Args:
        spark (SparkSession): The Spark session.
        catalog (str): The name of the catalog.
        namespace (str): The name of the namespace to ensure exists.
    """
    try:

        # Check if the namespace exists
        existing_namespaces = spark.sql(f"SHOW NAMESPACES IN {catalog}").collect()
        existing_namespace_names = [row[0] for row in existing_namespaces]

        if namespace not in existing_namespace_names:
            # Create the namespace if it does not exist
            spark.sql(f"CREATE NAMESPACE {catalog}.{namespace}")
            logger.info(f"Namespace '{namespace}' created in catalog '{catalog}'.") 
    except Exception as e:
        logger.error(f"Error ensuring namespace '{namespace}' exists in catalog '{catalog}': {e}")
        raise e

def build_iceberg_table_cols(schema: dict, column_type: str)-> list[str]:
    columns = []
    for column_name, column_config in schema.get(column_type, {}).items():
        datatype = TYPE_MAPPING[column_config["datatype"]]

        nullable = "" if column_config["nullable"] else "NOT NULL"

        columns.append(
            f"{column_name} {datatype} {nullable}".strip()
        )

    return columns


def generate_create_table_sql(
        catalog: str,
        namespace: str,
        table_name: str,
        schema: dict,
        logger=None                                             
):
    """
    Generate a CREATE TABLE SQL statement for the specified table with the given schema.

    Args:
        catalog (str): The name of the catalog.
        namespace (str): The name of the namespace.
        table_name (str): The name of the table to create.
        schema (dict): A dictionary representing the schema of the table, where keys are column names and values are data types.

    Returns:
        str: The generated CREATE TABLE SQL statement.
    """
    columns = []

    #business columns
    columns.extend(build_iceberg_table_cols(schema,"columns"))
    ##build_iceberg_table_cols(schema,"columns", columns)

    logger.info("Columns - business: %s", columns)

    #system columns
    columns.extend(build_iceberg_table_cols(schema,"system_columns"))
    logger.info("Columns - Full: %s", columns)

    """ 

    for column_name, column_config in schema["columns"].items():

        datatype = TYPE_MAPPING[column_config["datatype"]]

        nullable = "" if column_config["nullable"] else "NOT NULL"

        columns.append(
            f"{column_name} {datatype} {nullable}".strip()
        )
    
    """
    

    column_sql = ",\n".join(columns)
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {catalog}.{namespace}.{table_name} (
        {column_sql}
    )
    USING iceberg
    """
    
    return create_table_sql

def create_table_if_not_exists(
    spark,
    catalog,
    namespace,
    table_name,
    schema,
    logger

):
    sql = generate_create_table_sql(
        catalog,
        namespace,
        table_name,
        schema,
        logger
    )
    
    spark.sql(sql)





def write_to_iceberg(
    batch_df: DataFrame,
    batch_id: int,
    table_name: str,
    mode: str = "append",
    logger=None 
    
):
    """
    Generic Iceberg writer.

    Parameters
    ----------
    batch_df : DataFrame
        Current micro batch.

    batch_id : int
        Spark Structured Streaming batch id.

    table_name : str
        Fully qualified Iceberg table.

    mode : str
        append
        overwrite
        merge (future SCD2)
    """

    print("=" * 80)
    print(f"Processing Batch : {batch_id}")
    print(f"Target Table     : {table_name}")
    print(f"Write Mode       : {mode}")
    print("=" * 80)

    if batch_df.isEmpty():
        logger.info(f"Batch {batch_id} is empty. Skipping.")
        print(f"Batch {batch_id} is empty. Skipping.")
        return

    try:

        if mode == "append":

            (
                batch_df.writeTo(table_name)
                .append()
            )

        elif mode == "overwrite":

            (
                batch_df.writeTo(table_name)
                .overwritePartitions()
            )

        elif mode == "merge":
            error_msg = "Merge mode will be implemented during SCD2."
            if logger:
                logger.error(error_msg)

            raise NotImplementedError(
                "Merge mode will be implemented during SCD2."
            )

        else:
            error_msg = f"Unsupported write mode: {mode}"
            if logger:
                logger.error(error_msg)

            raise ValueError(
                f"Unsupported write mode: {mode}"
            )

        logger.info(f"Batch {batch_id} committed successfully.")

    except Exception as e:

        logger.error(f"Failed Batch : {batch_id}")

        raise e 