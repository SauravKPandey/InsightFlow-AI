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

def map_entity(cdc_df : DataFrame, entity_config: dict) -> DataFrame:
    
    print("Running Entity Mapper")
    #Fetch the entity schema from the entity configuration using the generate_schema function
    entity_schema = generate_schema(entity_config)

  

    #Map the CDC DataFrame to the entity-specific schema using selectExpr and aliasing
    entity_df = cdc_df.withColumn("after_struct", from_json(cdc_df["after_json"], entity_schema)) 

    #compare this business col method with the one below, which is more efficient and uses list comprehension to create the business columns
    #business_columns = [col_name for col_name in entity_config["columns"].keys()]

    #create business columns from metadata yaml file
    business_columns = [col(f"after_struct.{col_name}").alias(col_name) for col_name in entity_config["columns"].keys()]

    #Select the business columns from the entity DataFrame
    mapped_df = entity_df.select(*business_columns,
                                 col("topic"),
                                 col("partition"),
                                 col("offset"),
                                 col("timestamp")
                                )
    mapped_df = normalize(mapped_df, entity_config)
    print("Entity Mapping Completed")
                                                                                            

    return mapped_df