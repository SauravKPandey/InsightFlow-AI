
# Capacity Planning & Back-of-the-Envelope (BOE)

## Purpose

This document estimates expected platform scale, storage growth, throughput requirements, and validates architectural decisions for InsightFlow.

The objective is not to produce exact sizing but to ensure that the selected architecture can support expected business growth over the next 3–5 years.

---

# 1. Business Assumptions

## Business Context

InsightFlow is a global subscription-based digital platform providing:

* Revenue Analytics
* Subscription Analytics
* Product Usage Analytics
* Customer Health Analytics
* Churn Analytics
* Forecasting

---

## Current Scale

| Metric               |     Value |
| -------------------- | --------: |
| Customers            | 1,000,000 |
| Active Subscriptions | 5,000,000 |
| Products             |     1,000 |
| Pricing Plans        |       100 |

---

## Growth Assumption

Annual Growth Rate:

```text
25% YoY
```

---

## Five-Year Projection

| Metric        | Current |  Year 5 |
| ------------- | ------: | ------: |
| Customers     |   1.0 M |  3.05 M |
| Subscriptions |   5.0 M | 15.25 M |

---

# 2. User Activity Assumptions

## Daily Active Customers

Assumption:

```text
30%
```

Calculation:

```text
1,000,000 × 30%
=
300,000 Active Customers
```

---

## Users per Customer

Assumption:

```text
20 Users
```

Calculation:

```text
300,000 × 20
=
6,000,000 Active Users
```

---

## Events per Active User

Assumption:

```text
20 Events/User/Day
```

Examples:

* Login
* Search
* Browse
* Feature Usage
* Session Activity
* Content Consumption

---

## Total Daily Events

Calculation:

```text
6,000,000 × 20
=
120,000,000 Events/Day
```

---

# 3. Event Throughput Estimation

## Average Throughput

Calculation:

```text
120,000,000 / 86,400
≈ 1,400 Events/Sec
```

---

## Peak Throughput

Assumption:

```text
5x Peak Multiplier
```

Calculation:

```text
1,400 × 5
≈ 7,000 Events/Sec
```

---

# 4. Storage Assumptions

## Average Event Size

Assumption:

```text
1 KB/Event
```

This includes:

* Business Attributes
* Event Metadata
* Audit Information

---

## Annual Usage Event Volume

Calculation:

```text
120M × 365
=
43.8 Billion Events/Year
```

---

## Raw Annual Storage

Calculation:

```text
43.8 Billion × 1 KB
≈ 44 TB/Year
```

---

# 5. Estimated Annual Storage by Entity

| Table            | Estimated Annual Storage |
| ---------------- | -----------------------: |
| fact_usage_event |                   ~50 TB |
| fact_invoice     |                 ~0.06 TB |
| fact_payment     |                 ~0.06 TB |
| dim_customer     |                ~0.003 TB |
| dim_subscription |                 ~0.01 TB |
| Other Dimensions |               Negligible |

---

## Silver Layer Total

Estimated:

```text
50–55 TB/Year
```

---

# 6. Retention Estimates

## GCS Raw Archive

Retention:

```text
7 Years
```

Storage:

```text
~300 TB
```

---

## Silver Layer

Retention:

```text
Indefinite
```

Five-Year Estimate:

```text
~250–275 TB
```

Seven-Year Estimate:

```text
~350–400 TB
```

---

# 7. Key Capacity Insights

## Insight 1

Usage events are the dominant workload.

```text
95%+ of platform storage
=
fact_usage_event
```

---

## Insight 2

Dimension tables contribute negligible storage relative to fact tables.

```text
Customer

Subscription

Pricing Plan
```

storage remains small even with SCD Type 2.

---

## Insight 3

Storage growth is manageable within BigQuery.

Projected data volumes remain well within BigQuery operational limits.

---

# 8. Architecture Validation

## Kafka

Status:

```text
VALIDATED
```

Reason:

```text
120M Events/Day

~7K Peak Events/Sec
```

Kafka comfortably supports projected throughput.

---

## BigQuery

Status:

```text
VALIDATED
```

Reason:

```text
50–55 TB Annual Growth

Hundreds of TB Retained
```

BigQuery remains an appropriate analytical platform.

---

## Airflow

Status:

```text
VALIDATED
```

Reason:

```text
Moderate DAG Count

Entity-Based Orchestration
```

No scaling concerns identified.

---

## Lakehouse Architecture

Status:

```text
DEFERRED
```

Reason:

```text
Current scale does not justify
Iceberg / Delta / Spark complexity.
```

May be revisited in future phases.

---

# 9. Architectural Decisions Influenced by BOE

Validated Decisions:

* Kafka-based event streaming
* BigQuery analytical warehouse
* GCS raw archive retention
* SCD Type 2 dimensions
* Partitioned fact tables
* Clustered usage event tables
* Gold-layer aggregate strategy

---

# Conclusion

The projected business scale, throughput requirements, and storage growth validate the selected InsightFlow architecture:

```text
Kafka
    ↓
GCS Landing
    ↓
BigQuery Bronze
    ↓
BigQuery Silver
    ↓
BigQuery Gold
```

The architecture is expected to support projected growth over the next five years without requiring significant redesign.

---

Document Status

Version: 1.0

Status: APPROVED
