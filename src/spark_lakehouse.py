from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

PROCESSED_PATH = Path("data/processed/cleaned_online_retail.csv")
BRONZE_PATH = "data/spark_lakehouse/bronze/sales"
SILVER_PATH = "data/spark_lakehouse/silver/sales"
GOLD_MONTHLY_PATH = "data/spark_lakehouse/gold/monthly_revenue"
GOLD_COUNTRY_PATH = "data/spark_lakehouse/gold/country_revenue"


def create_spark():
    return (
        SparkSession.builder.appName("retail-spark-lakehouse")
        .config("spark.sql.shuffle.partitions", "8")
        .config("spark.sql.adaptive.enabled", "true")
        .getOrCreate()
    )


def read_processed_sales(spark):
    return (
        spark.read.option("header", True)
        .option("inferSchema", True)
        .csv(str(PROCESSED_PATH))
        .withColumn("invoice_date", F.to_timestamp("invoice_date"))
        .withColumn("order_date", F.to_date("invoice_date"))
        .withColumn("year_month", F.date_format("invoice_date", "yyyy-MM"))
    )


def write_bronze(df):
    (
        df.write.mode("overwrite")
        .partitionBy("year_month")
        .parquet(BRONZE_PATH)
    )


def write_silver(df):
    silver_df = (
        df.filter(
            (F.col("quantity") > 0)
            & (F.col("unit_price") > 0)
            & (F.col("is_cancelled") == F.lit(False))
        )
        .withColumn("total_amount", F.col("quantity") * F.col("unit_price"))
        .repartition("year_month")
    )

    (
        silver_df.write.mode("overwrite")
        .partitionBy("year_month")
        .parquet(SILVER_PATH)
    )

    return silver_df


def write_gold(silver_df):
    monthly_revenue = (
        silver_df.groupBy("year_month")
        .agg(F.round(F.sum("total_amount"), 2).alias("revenue"))
        .orderBy("year_month")
    )

    country_revenue = (
        silver_df.groupBy("country")
        .agg(F.round(F.sum("total_amount"), 2).alias("revenue"))
        .orderBy(F.desc("revenue"))
    )

    monthly_revenue.coalesce(1).write.mode("overwrite").parquet(GOLD_MONTHLY_PATH)
    country_revenue.coalesce(1).write.mode("overwrite").parquet(GOLD_COUNTRY_PATH)


def main():
    spark = create_spark()
    try:
        bronze_df = read_processed_sales(spark)
        write_bronze(bronze_df)
        silver_df = write_silver(bronze_df)
        write_gold(silver_df)
        print("Spark lakehouse pipeline completed successfully!")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
