from pyspark.sql import DataFrame
from pyspark.sql.functions import current_timestamp


def update_replay_status(
    spark,
    replay_df: DataFrame,
    dlq_table: str,
    logger
):

    if replay_df.isEmpty():
        logger.info("No replay status updates required.")
        return

    
    replay_df = replay_df.localCheckpoint(eager=True)
    temp_view = "replay_updates"
    replay_df.count()  # Force evaluation to avoid lazy execution issues

    replay_df.createOrReplaceTempView(temp_view)



    merge_sql = f"""
        MERGE INTO {dlq_table} t
        USING {temp_view} s

        ON t.event_id = s.event_id

        WHEN MATCHED THEN
        UPDATE SET

            t.retry_count = t.retry_count + 1,
            t.replay_status = s.replay_status,
            t.replay_timestamp = current_timestamp()

    """

    logger.info("Updating Replay Status")

    spark.sql(merge_sql)

    logger.info("Replay Status Updated")