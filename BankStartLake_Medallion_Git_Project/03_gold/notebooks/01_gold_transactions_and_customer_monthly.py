# Databricks notebook source
# MAGIC %md
# MAGIC # Gold — Business-ready Transaction and Customer Analytics
# MAGIC
# MAGIC Gold should expose stable datasets for BI/reporting rather than raw engineering fields.

from pyspark.sql import functions as F

SILVER = "workspace.silver.transactions"
GOLD_FACT = "workspace.gold.fact_transactions"
GOLD_CUSTOMER_MONTHLY = "workspace.gold.customer_monthly"

silver = spark.table(SILVER)

# Business-ready transaction fact.
fact = (
    silver
    .select(
        "transaction_id",
        "customer_id",
        "transaction_date",
        "updated_at",
        "transaction_amount",
        "merchant_code",
        "category",
        "points_posted",
        "points_redeemed"
    )
)

# Demo write. In production, use incremental MERGE where appropriate.
# fact.write.format("delta").mode("overwrite").saveAsTable(GOLD_FACT)

customer_monthly = (
    silver
    .withColumn(
        "transaction_month",
        F.date_trunc("month", F.col("transaction_date"))
    )
    .groupBy("customer_id", "transaction_month")
    .agg(
        F.countDistinct("transaction_id").alias("transaction_count"),
        F.sum("transaction_amount").alias("total_transaction_amount"),
        F.avg("transaction_amount").alias("avg_transaction_amount"),
        F.sum("points_posted").alias("total_points_posted"),
        F.sum("points_redeemed").alias("total_points_redeemed"),
        F.max("transaction_date").alias("last_transaction_date")
    )
)

# customer_monthly.write.format("delta").mode("overwrite").saveAsTable(
#     GOLD_CUSTOMER_MONTHLY
# )

print("Gold fact and customer-monthly aggregation prepared.")
