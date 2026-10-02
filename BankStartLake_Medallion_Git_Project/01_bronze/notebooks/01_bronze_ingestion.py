# Databricks notebook source
# MAGIC %md
# MAGIC # Bronze Ingestion
# MAGIC
# MAGIC Purpose:
# MAGIC - Preserve source data
# MAGIC - Add ingestion metadata
# MAGIC - Append data without business transformations
# MAGIC - Keep Bronze replayable/auditable

from pyspark.sql import functions as F

SOURCE_PATH = "<BANK_SOURCE_PATH>"
BRONZE_TABLE = "workspace.bronze.transactions"

# Example source read:
# raw_df = (
#     spark.read
#     .option("header", True)
#     .option("inferSchema", False)
#     .csv(SOURCE_PATH)
# )

# Example batch identifier supplied by ADF/Databricks Job:
batch_id = "<BATCH_ID>"

# bronze_df = (
#     raw_df
#     .withColumn("_ingestion_timestamp", F.current_timestamp())
#     .withColumn("_batch_id", F.lit(batch_id))
#     .withColumn("_source_file", F.input_file_name())
# )

# Keep Bronze source-preserving.
# bronze_df.write.format("delta").mode("append").saveAsTable(BRONZE_TABLE)

print(f"Target Bronze table: {BRONZE_TABLE}")
