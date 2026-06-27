from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("ReadBronze")
    .getOrCreate()
)

df = spark.read.parquet("data/bronze/customer")

df.printSchema()

df.show(1, truncate=False)