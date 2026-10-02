# Simulation Scenarios

Use synthetic data to demonstrate incremental processing and explain the architecture during interviews.

## Recommended Test Batch

Create a test batch with:

- 5 new transactions
- 3 updates to existing transaction IDs
- 2 exact duplicates/re-ingestion records
- 1 late-arriving transaction
- 1 bad transaction failing DQ

## Expected Behaviour

| Scenario | Expected Silver Behaviour |
|---|---|
| New transaction | Insert |
| Updated transaction | Replace only if `updated_at` is newer |
| Exact duplicate | No duplicate Silver record |
| Late-arriving record | Process using technical timestamp/watermark strategy |
| Bad record | Quarantine in rejected table |
| Replay same batch | Idempotent; no duplicate result |

Do not commit real customer/bank data to Git. Generate synthetic data in Databricks or keep local files ignored by `.gitignore`.
