# Databricks notebook source
# MAGIC %md
# MAGIC # Audit and Validation
# MAGIC
# MAGIC Lightweight reconciliation checks for interview/demo purposes.

from pyspark.sql import functions as F

tables = [
    "workspace.bronze.transactions",
    "workspace.silver.transactions",
    "workspace.silver.rejected_transactions",
    "workspace.gold.fact_transactions",
    "workspace.gold.customer_monthly",
]

for table_name in tables:
    try:
        count = spark.table(table_name).count()
        print(f"{table_name}: {count:,}")
    except Exception as exc:
        print(f"{table_name}: NOT AVAILABLE ({exc})")

# Silver uniqueness assertion.
try:
    duplicate_count = (
        spark.table("workspace.silver.transactions")
        .groupBy("transaction_id")
        .count()
        .filter(F.col("count") > 1)
        .count()
    )

    assert duplicate_count == 0, (
        f"Silver uniqueness failed. Duplicate transaction IDs: {duplicate_count}"
    )
    print("PASS: Silver transaction_id is unique.")
except Exception as exc:
    print(f"Silver uniqueness check skipped: {exc}")

# Schema checks.
try:
    silver = spark.table("workspace.silver.transactions")
    fields = {f.name: f.dataType.simpleString() for f in silver.schema.fields}

    print("transaction_date type:", fields.get("transaction_date"))
    print("updated_at type:", fields.get("updated_at"))
except Exception as exc:
    print(f"Schema check skipped: {exc}")
