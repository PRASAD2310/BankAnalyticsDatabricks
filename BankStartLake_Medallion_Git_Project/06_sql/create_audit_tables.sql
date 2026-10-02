-- BankStartLake audit tables
-- Databricks SQL / Delta

CREATE TABLE IF NOT EXISTS workspace.audit.pipeline_audit (
    batch_id STRING,
    pipeline_name STRING,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    source_count BIGINT,
    processed_count BIGINT,
    rejected_count BIGINT,
    duplicate_count BIGINT,
    status STRING,
    watermark_before TIMESTAMP,
    watermark_after TIMESTAMP,
    error_message STRING
) USING DELTA;

CREATE TABLE IF NOT EXISTS workspace.audit.dq_rule_audit (
    batch_id STRING,
    rule_name STRING,
    total_records BIGINT,
    passed_records BIGINT,
    rejected_records BIGINT,
    execution_time TIMESTAMP
) USING DELTA;
