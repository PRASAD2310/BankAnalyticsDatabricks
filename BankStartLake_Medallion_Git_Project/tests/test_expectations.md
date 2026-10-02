# Test Expectations

1. `transaction_id` is unique in Silver.
2. `transaction_date` is a DATE.
3. `updated_at` is a TIMESTAMP.
4. Invalid records are present in the rejected table with a DQ reason.
5. New records are inserted into Silver.
6. Newer updates replace older versions.
7. Older updates do not overwrite newer records.
8. Exact replay does not create duplicate Silver records.
9. Late-arriving data is handled using the incremental strategy.
10. Gold totals reconcile with valid Silver data.
11. DQ audit counts reconcile with accepted + rejected records.
12. Watermark is not advanced when the pipeline fails.
