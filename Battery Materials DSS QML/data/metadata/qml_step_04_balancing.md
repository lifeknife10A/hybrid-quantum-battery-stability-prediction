# QML Step 04: Balancing

Generated on: 2026-06-28

## Reason

The full dataset has many more unstable materials than stable materials. If we
train directly on that imbalance, the model may learn to predict unstable too
often.

## Clean Dataset Class Counts

| target_is_stable | count | percentage |
| --- | --- | --- |
| 0 | 20016 | 83.16 |
| 1 | 4052 | 16.84 |

## Balancing Rule

- Maximum rows per class: 500
- Actual rows per class used: 500
- Random state: 42

## Balanced Dataset Class Counts

| target_is_stable | count | percentage |
| --- | --- | --- |
| 0 | 500 | 50 |
| 1 | 500 | 50 |

## Output Of This Step

- Balanced rows: 1,000
- Stable rows: 500
- Unstable rows: 500
