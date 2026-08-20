from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    LongType
)
from framework.metadata.schema_generator import generate_schema
from pyspark.sql import DataFrame
from pyspark.sql.functions import from_json, col
from framework.transformation.normalizer import normalize

def map_entity(cdc_df : DataFrame, entity_config: dict, logger=None, replay = False) -> DataFrame:
    
    logger.info("Running Entity Mapper")
    #Fetch the entity schema from the entity configuration using the generate_schema function
    entity_schema = generate_schema(entity_config, logger=logger)

  

    #Map the CDC DataFrame to the entity-specific schema using selectExpr and aliasing
    entity_df = cdc_df.withColumn("after_struct", from_json(cdc_df["after_json"], entity_schema)) 

    #compare this business col method with the one below, which is more efficient and uses list comprehension to create the business columns
    #business_columns = [col_name for col_name in entity_config["columns"].keys()]

    #create business columns from metadata yaml file
    business_columns = [col(f"after_struct.{col_name}").alias(col_name) for col_name in entity_config["columns"].keys()]
    system_columns = [col(column_name) for column_name in entity_config.get("system_columns", {})]

    #Select the business columns from the entity DataFrame
    if replay:
        mapped_df = entity_df.select(*business_columns,
                                    *system_columns,
                                    col("event_id"),
                                    col("topic"),
                                    col("partition"),
                                    col("offset"),
                                    col("timestamp"),
                                    col("key"),
                                    col("raw_payload"),
                                    col("timestampType")
                                    )
    else:
        mapped_df = entity_df.select(*business_columns,
                                            *system_columns,
                                            #col("event_id"),
                                            col("topic"),
                                            col("partition"),
                                            col("offset"),
                                            col("timestamp"),
                                            col("key"),
                                            col("raw_payload"),
                                            col("timestampType")
                                            )
    ''' 
    mapped_df.printSchema()

    mapped_df.select(
        "op",
        "ts_ms"
    ).show(truncate=False)
    '''

    mapped_df = normalize(mapped_df, entity_config, logger=logger)
    logger.info("Entity Mapping Completed")

    '''

    mapped_df.select(
        "op",
        "ts_ms"
    ).show(truncate=False)

    '''
                                                                                            

    return mapped_df