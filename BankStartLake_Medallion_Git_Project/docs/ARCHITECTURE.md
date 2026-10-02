# Architecture Notes

## Bronze

Bronze is the source-preservation layer. The goal is traceability and replayability, not business transformation.

Typical metadata:
- `_ingestion_timestamp`
- `_batch_id`
- `_source_file`

## Silver

Silver creates trusted analytical records.

Typical processing:
1. Incremental read based on `updated_at`.
2. Schema normalization.
3. Explicit date/timestamp parsing.
4. Null/range/domain validation.
5. Rejected-record quarantine.
6. Deduplication.
7. Latest-version selection.
8. Delta MERGE.

## Gold

Gold contains business-ready datasets optimized for analytics and BI.

Examples:
- Transaction fact
- Customer monthly summary
- Reward/redemption metrics
- Campaign/customer segmentation datasets

## Incremental Strategy

Use a technical watermark such as `updated_at`, not only business date.

A small lookback window can protect against late-arriving updates:

```text
last_successful_watermark - lookback
```

The pipeline should advance the watermark only after the required processing and reconciliation steps succeed.

## Late-arriving Data

Business date and technical update time are different concepts:

- `transaction_date`: when the business transaction happened.
- `updated_at`: when the source record was created/changed.

This allows late-arriving transactions to be processed without incorrectly treating them as current-day business activity.

## Production Hardening

A production implementation can add:
- Unity Catalog permissions
- Secret scopes/key vault integration
- ADF/Databricks Jobs orchestration
- CI/CD
- Schema evolution controls
- DQ thresholds and alerts
- Pipeline monitoring
- Data lineage
- File/API source audit
- Partitioning/Z-Ordering where justified
- Auto Loader for file ingestion
- Retry and dead-letter handling
