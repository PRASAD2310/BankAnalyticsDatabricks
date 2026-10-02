-- Basic reconciliation queries

SELECT COUNT(*) AS bronze_count
FROM workspace.bronze.transactions;

SELECT COUNT(*) AS silver_count
FROM workspace.silver.transactions;

SELECT COUNT(*) AS rejected_count
FROM workspace.silver.rejected_transactions;

SELECT transaction_id, COUNT(*) AS cnt
FROM workspace.silver.transactions
GROUP BY transaction_id
HAVING COUNT(*) > 1;

SELECT COUNT(*) AS gold_count
FROM workspace.gold.fact_transactions;

SELECT *
FROM workspace.audit.pipeline_audit
ORDER BY start_time DESC;

SELECT *
FROM workspace.audit.dq_rule_audit
ORDER BY execution_time DESC;
