from pyspark.sql import SparkSession
from common.config_loader import load_config


def create_spark_session(app_name: str, env:str):
    env_config = load_config(env)

    credentials_path = env_config["gcp"]["credentials_path"]
    spark_packages = ",".join(env_config["spark"]["packages"])

    spark = (
        SparkSession.builder
        .appName(app_name)
        .config("spark.jars.packages", spark_packages)

        # ---------- GCS ----------
        .config(
            "spark.hadoop.fs.gs.impl",
            "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem"
        )
        .config(
            "spark.hadoop.fs.AbstractFileSystem.gs.impl",
            "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS"
        )

        # Tell GCS connector to use ADC
        .config(
            "spark.hadoop.google.cloud.auth.service.account.enable",
            "true"
        )
        .config(
            "spark.hadoop.google.cloud.auth.service.account.json.keyfile",
            credentials_path
        )
        .config(
            "spark.sql.extensions",
            "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions"
        )
        # Iceberg Catalog
        .config(
            "spark.sql.catalog.insightflow",
            "org.apache.iceberg.spark.SparkCatalog"
        )
        .config(
            "spark.sql.catalog.insightflow.type",
            "hadoop"
        )
        .config(
            "spark.sql.catalog.insightflow.warehouse",
            env_config["iceberg"]["warehouse"]
        )


        .getOrCreate()
    )

    return spark