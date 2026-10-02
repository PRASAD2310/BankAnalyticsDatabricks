# Runbook

## Normal Run

1. Receive source batch/file/API data.
2. Write raw data to Bronze.
3. Read the last successful watermark.
4. Select the incremental window.
5. Normalize schema and timestamps.
6. Apply DQ rules.
7. Write rejected records.
8. Deduplicate valid records.
9. MERGE latest versions into Silver.
10. Refresh/merge Gold datasets.
11. Run reconciliation checks.
12. Write pipeline and DQ audit records.
13. Advance watermark only after successful completion.

## DQ Failure

Inspect:
- `workspace.silver.rejected_transactions`
- `workspace.audit.dq_rule_audit`
- source batch identifier

Do not silently discard bad records.

## MERGE Failure

Do not advance the watermark if the required processing has failed. The batch should remain safely replayable.

## Replay

Reprocessing the same batch should not create duplicate Silver records.

This is one of the main idempotency behaviours demonstrated by this project.
