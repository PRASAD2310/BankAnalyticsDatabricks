

> I implemented a medallion architecture in Databricks where Bronze preserves source data, Silver performs schema normalization, data-quality validation, deduplication and incremental Delta MERGE processing, and Gold exposes business-ready transaction and customer analytics. I also maintained DQ and pipeline audit tables and tested new records, updates, duplicates, late-arriving records and bad records. 

# BankStartLake — Medallion Architecture Data Engineering Project
Databricks/PySpark project demonstrating a production-style **Bronze → Silver → Gold** lakehouse architecture for bank transaction and rewards data.

## Business Scenario

A bank provides transaction data through batch files/APIs. The platform must preserve raw source data, validate and standardize it, handle duplicates and updates, and expose trusted business datasets for reporting and customer analytics.

## Architecture

```text
Bank Files / APIs
       |
       v
+------------------+
| BRONZE           |
| Raw / Immutable  |
| Source Preserve  |
+------------------+
       |
       | Incremental + Watermark
       v
+------------------+
| SILVER           |
| DQ + Normalize   |
| Dedup + MERGE    |
| Reject Quarantine|
+------------------+
       |
       v
+------------------+
| GOLD             |
| Fact Transactions|
| Customer Monthly |
| Business Metrics |
+------------------+

        +----------------------+
        | AUDIT / DQ           |
        | Pipeline Audit       |
        | Rule-level Audit     |
        +----------------------+
```

## Databricks Tables

| Layer | Table | Purpose |
|---|---|---|
| Bronze | `workspace.bronze.transactions` | Raw source-preserving transaction data |
| Silver | `workspace.silver.transactions` | Validated, normalized, latest transaction version |
| Silver | `workspace.silver.rejected_transactions` | DQ failures/quarantined records |
| Gold | `workspace.gold.fact_transactions` | Business-ready transaction fact |
| Gold | `workspace.gold.customer_monthly` | Customer monthly analytics |
| Audit | `workspace.audit.dq_rule_audit` | DQ rule execution metrics |
| Audit | `workspace.audit.pipeline_audit` | Batch/pipeline execution audit |

## Key Engineering Concepts Demonstrated

- Medallion architecture
- PySpark transformations
- Delta Lake
- Incremental processing
- Watermark strategy
- Late-arriving data
- Explicit date/timestamp parsing
- Data quality and quarantine
- Deduplication using `row_number`
- Latest-record selection using `updated_at`
- Delta `MERGE`
- Idempotent reprocessing
- Audit/reconciliation
- Business date vs technical processing timestamp
- Gold-layer aggregation
- Production considerations for Unity Catalog, CI/CD, secrets and monitoring




## Important Design Decisions

- Bronze is append-only/source-preserving.
- Silver keeps the latest valid version for each `transaction_id`.
- `transaction_date` is the business date.
- `updated_at` is the technical change timestamp used for incremental processing.
- Invalid records are quarantined rather than silently dropped.
- Watermark is advanced only after successful processing.
- Replaying the same batch should not create duplicate Silver records.
- Synthetic/demo data only; no credentials or customer data should be committed.

