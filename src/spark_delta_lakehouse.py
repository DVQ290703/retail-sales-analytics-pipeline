from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

PROCESSED_PATH = Path("data/processed/cleaned_online_retail.csv")
DELTA_ROOT = "data/delta_lakehouse"
BRONZE_TABLE = f"{DELTA_ROOT}/bronze/sales"
SILVER_TABLE = f"{DELTA_ROOT}/silver/sales"
GOLD_MONTHLY_TABLE = f"{DELTA_ROOT}/gold/monthly_revenue"


def create_spark():
    return (
        SparkSession.builder.appName("retail-delta-lakehouse")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
        .config("spark.sql.shuffle.partitions", "8")
        .config("spark.sql.adaptive.enabled", "true")
        .getOrCreate()
    )


def read_sales(spark):
    return (
        spark.read.option("header", True)
        .option("inferSchema", True)
        .csv(str(PROCESSED_PATH))
        .withColumn("invoice_date", F.to_timestamp("invoice_date"))
        .withColumn("year_month", F.date_format("invoice_date", "yyyy-MM"))
    )


def write_delta_table(df, path, partition_columns=None):
    writer = df.write.format("delta").mode("overwrite")
    if partition_columns:
        writer = writer.partitionBy(*partition_columns)
    writer.save(path)


def main():
    spark = create_spark()
    try:
        bronze_df = read_sales(spark)
        write_delta_table(bronze_df, BRONZE_TABLE, ["year_month"])

        silver_df = (
            bronze_df.filter(
                (F.col("quantity") > 0)
                & (F.col("unit_price") > 0)
                & (F.col("is_cancelled") == F.lit(False))
            )
            .withColumn("total_amount", F.col("quantity") * F.col("unit_price"))
            .repartition("year_month")
        )
        write_delta_table(silver_df, SILVER_TABLE, ["year_month"])

        monthly_revenue = (
            silver_df.groupBy("year_month")
            .agg(F.round(F.sum("total_amount"), 2).alias("revenue"))
            .orderBy("year_month")
        )
        write_delta_table(monthly_revenue, GOLD_MONTHLY_TABLE)

        history = spark.sql(f"DESCRIBE HISTORY delta.`{SILVER_TABLE}`")
        history.select("version", "operation", "timestamp").show(truncate=False)
        print("Delta lakehouse pipeline completed successfully!")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
