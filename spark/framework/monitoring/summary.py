from pyspark.sql import DataFrame
from pyspark.sql.functions import col, explode

from framework.logging.logger import get_logger
from framework.validation.constants import VALIDATION_ERROR_COLUMN

logger = get_logger(__name__)


def summarize(
    valid_df: DataFrame,
    invalid_df: DataFrame,
    entity_name: str,
    batch_id: int
) -> dict:
    """
    Log validation summary for every micro-batch.

    Returns
    -------
    dict
        Validation metrics for downstream consumers
        (Alert Manager, Monitoring, Dashboard etc.)
    """

    valid_count = valid_df.count()
    invalid_count = invalid_df.count()
    total_count = valid_count + invalid_count

    failure_pct = (
        (invalid_count / total_count) * 100
        if total_count > 0
        else 0.0
    )

    logger.info("=" * 80)
    logger.info("VALIDATION SUMMARY")
    logger.info("=" * 80)
    logger.info(f"Entity             : {entity_name}")
    logger.info(f"Batch ID           : {batch_id}")
    logger.info(f"Total Records      : {total_count}")
    logger.info(f"Valid Records      : {valid_count}")
    logger.info(f"Invalid Records    : {invalid_count}")
    logger.info(f"Failure Percentage : {failure_pct:.2f}%")

    validation_breakdown = {}

    if invalid_count == 0:

        logger.info("Validation Breakdown")
        logger.info("No validation failures detected.")

    else:

        rule_summary = (
            invalid_df
            .select(explode(col(VALIDATION_ERROR_COLUMN)).alias("error"))
            .groupBy("error.rule")
            .count()
            .collect()
        )

        logger.info("Validation Breakdown")

        for row in rule_summary:

            validation_breakdown[row["rule"]] = row["count"]

            logger.info(
                f"{row['rule']:<25}: {row['count']}"
            )

    logger.info("=" * 80)

    return {

        "entity_name": entity_name,

        "batch_id": batch_id,

        "total_records": total_count,

        "valid_records": valid_count,

        "invalid_records": invalid_count,

        "failure_percentage": failure_pct,

        "validation_breakdown": validation_breakdown

    }