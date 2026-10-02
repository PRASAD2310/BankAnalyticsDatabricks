# Data Model

## Bronze

**Grain:** one source transaction/version.

The layer preserves source attributes plus ingestion metadata.

## Silver Transactions

**Grain:** latest valid version per `transaction_id`.

Important fields:
- transaction_id
- customer_id
- transaction_date
- updated_at
- transaction_amount
- merchant_code
- category
- points_posted
- points_redeemed

## Silver Rejected Transactions

Contains records failing DQ with:
- original source fields
- `dq_rule`
- `dq_reason`
- `rejected_at`

## Gold Fact Transactions

Business-facing transaction grain.

Engineering-only ingestion fields should generally be removed unless required for analytics.

## Gold Customer Monthly

**Grain:** one customer per transaction month.

Typical metrics:
- transaction_count
- total_transaction_amount
- avg_transaction_amount
- total_points_posted
- total_points_redeemed
- last_transaction_date
