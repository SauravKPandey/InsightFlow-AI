from pyspark.sql import DataFrame
from pyspark.sql.functions import get_json_object, col

def parse_debezium(bronze_decoded_df: DataFrame, logger=None) -> DataFrame:

    print("Running Debezium Parser")
    """
    Input: Bronze cdc event
    O/P: 
        Columns:
            Key
            Value
            topic
            partition
            offset
            timestamp
    Returns:
        cdc_df
        columns:
            before
            after
            op
            source
            ts_ms
            topic
            partition
            off_Set
            timestamp

            raw_payload
    """
    cdc_df = bronze_decoded_df.select(

        get_json_object(
            col("raw_payload"),
            "$.payload.before"
        ).alias("before_json"),

        get_json_object(
            col("raw_payload"),
            "$.payload.after"
        ).alias("after_json"),

        get_json_object(
            col("raw_payload"),
            "$.payload.op"
        ).alias("op"),

        get_json_object(
            col("raw_payload"),
            "$.payload.ts_ms"
        ).alias("ts_ms"),

        get_json_object(
            col("raw_payload"),
            "$.payload.source"
        ).alias("source_json"),

        col("topic"),
        col("partition"),
        col("offset"),
        col("timestamp"),

        col("raw_payload")
    )
    logger.info("Debezium Parser Completed")
    #Test timestamp col values
    '''
    cdc_df.select(get_json_object(col("after_json"), "$.created_timestamp").alias("created_timestamp")).show(5, truncate=False)
    cdc_df.select(get_json_object(col("after_json"), "$.updated_timestamp").alias("updated_timestamp")).show(5, truncate=False)
    cdc_df.select(get_json_object(col("after_json"), "$.customer_start_date").alias("customer_start_date")).show(5, truncate=False)
    cdc_df.select(get_json_object(col("after_json"), "$.customer_end_date").alias("customer_end_date")).show(5, truncate=False)
                
    cdc_df.printSchema()

    cdc_df.select(
    "op",
    "ts_ms",
    "after_json"
    ).show(truncate=False) 
    '''   
    return cdc_df