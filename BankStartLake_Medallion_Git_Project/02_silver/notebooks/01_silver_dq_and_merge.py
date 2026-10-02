# Databricks notebook source
# MAGIC %md
# MAGIC # Silver — DQ, Deduplication and Incremental MERGE
# MAGIC
# MAGIC Processing sequence:
# MAGIC 1. Read Bronze
# MAGIC 2. Normalize date/timestamp fields
# MAGIC 3. Apply DQ rules
# MAGIC 4. Quarantine rejected records
# MAGIC 5. Deduplicate by transaction_id + latest updated_at
# MAGIC 6. MERGE into Silver
# MAGIC
# MAGIC Note: Explicit parsing patterns avoid silent date-format assumptions.

from pyspark.sql import functions as F
from pyspark.sql.window import Window
from delta.tables import DeltaTable

BRONZE = "workspace.bronze.transactions"
SILVER = "workspace.silver.transactions"
REJECTED = "workspace.silver.rejected_transactions"

df = spark.table(BRONZE)

# Normalize business date.
df = df.withColumn(
    "transaction_date",
    F.coalesce(
        F.to_date("transaction_date", "dd-MM-yyyy"),
        F.to_date("transaction_date", "yyyy-MM-dd")
    )
)

# Normalize technical timestamp.
df = df.withColumn(
    "updated_at",
    F.coalesce(
        F.to_timestamp("updated_at", "dd-MM-yyyy HH:mm"),
        F.to_timestamp("updated_at", "yyyy-MM-dd HH:mm:ss"),
        F.to_timestamp("updated_at", "yyyy-MM-dd'T'HH:mm:ss")
    )
)

# Example transaction-level DQ.
dq_condition = (
    F.col("transaction_id").isNull()
    | F.col("customer_id").isNull()
    | F.col("transaction_date").isNull()
    | F.col("transaction_amount").isNull()
    | (F.col("transaction_amount") < 0)
)

rejected = (
    df.filter(dq_condition)
      .withColumn("dq_rule", F.lit("MANDATORY_OR_INVALID_TRANSACTION_FIELDS"))
      .withColumn("dq_reason", F.lit("Failed transaction-level validation"))
      .withColumn("rejected_at", F.current_timestamp())
)

valid = df.filter(~dq_condition)

# Latest version wins for the business key.
window_spec = (
    Window
    .partitionBy("transaction_id")
    .orderBy(F.col("updated_at").desc_nulls_last())
)

latest = (
    valid
    .withColumn("_rn", F.row_number().over(window_spec))
    .filter(F.col("_rn") == 1)
    .drop("_rn")
)

# Initial creation example:
# latest.write.format("delta").mode("overwrite").saveAsTable(SILVER)
# rejected.write.format("delta").mode("append").saveAsTable(REJECTED)

# Incremental MERGE example:
#
# target = DeltaTable.forName(spark, SILVER)
#
# (
#     target.alias("t")
#     .merge(
#         latest.alias("s"),
#         "t.transaction_id = s.transaction_id"
#     )
#     .whenMatchedUpdateAll(
#         condition="s.updated_at > t.updated_at"
#     )
#     .whenNotMatchedInsertAll()
#     .execute()
# )

print("Silver DQ + dedup + MERGE pattern prepared.")
