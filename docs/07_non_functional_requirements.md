# 07_non_functional_requirements.md

# Non-Functional Requirements (NFR)

## Purpose

This document defines the operational, performance, scalability, reliability, security, and maintainability requirements for InsightFlow.

These requirements establish measurable expectations for the platform beyond functional business capabilities.

---

# 1. Availability Requirements

## Platform Availability

Target:


99.9%


Availability Window:


24x7


Excluding:


Planned Maintenance Windows


---

## Business Reporting Availability

Target:


99.9%


Business users shall have continuous access to Gold datasets and dashboards.

---

# 2. Performance Requirements

## Dashboard Response Time

Target:


< 5 seconds


For:


Executive Dashboards

KPI Dashboards

Operational Dashboards


---

## Ad Hoc Query Performance

Target:


< 30 seconds


For:


Business User Queries


---

## Data Load Performance

Bronze Load:


< 5 minutes


after data arrival.

---

## KPI Refresh Performance

Target:


< 1 hour


after source availability.

---

# 3. Scalability Requirements

## Data Volume Growth

Platform shall support:


10x growth


without architectural redesign.

---

## Storage Scalability

Architecture shall support:


Multi-terabyte datasets


using BigQuery native scaling.

---

## Event Scalability

Kafka shall support:


Millions of events per day


without redesign.

---

# 4. Reliability Requirements

## Pipeline Success Rate

Target:


> 99%


successful executions.

---

## Retry Capability

All pipelines shall support:


Automatic Retry

Manual Restart


---

## Data Recovery

All data shall be recoverable through:


GCS Raw Archive

Backfill Framework


---

# 5. Recoverability Requirements

## Raw Data Retention

Target:


7 Years


---

## Backfill Support

All pipelines shall support:


Date Range Reprocessing


---

## Disaster Recovery

Target:


Platform recoverable from raw source data.


---

# 6. Security Requirements

## Authentication

Access shall be integrated with:


Google IAM


---

## Authorization

Access shall follow:


Role-Based Access Control (RBAC)


---

## Encryption

Data In Transit:


TLS


Data At Rest:


Google Managed Encryption


---

# 7. Data Quality Requirements

## DQ Score

Target:


≥ 95%


for production datasets.

---

## Data Validation

Required Checks:


Completeness

Uniqueness

Validity

Consistency

Referential Integrity


---

# 8. Observability Requirements

## Monitoring Coverage

All pipelines shall provide:


Execution Metrics

DQ Metrics

Freshness Metrics

Alert Metrics


---

## Metadata Tracking

Mandatory:


pipeline_run

pipeline_watermark

data_quality_results

alert_log


---

# 9. Maintainability Requirements

## Metadata Driven Design

Pipeline configuration shall be externalized wherever possible.

---

## Standardized Naming

All datasets, tables, and columns shall follow approved naming conventions.

---

## Reusability

Pipeline components shall be reusable across domains.

---

# 10. Auditability Requirements

## Data Lineage

Lineage shall be traceable from:


Source System

Kafka Topic

GCS Landing

Bronze

Silver

Gold

Dashboard


---

## Audit Logs

Minimum Retention:


1 Year


---

# 11. Compliance Requirements

## Data Retention

| Layer           | Retention   |
| --------------- | ----------- |
| GCS Raw Archive | 7 Years     |
| Bronze          | 7 Years     |
| Silver          | Indefinite  |
| Gold            | Rebuildable |
| Metadata        | 3 Years     |

---

## Sensitive Data

PII shall be protected through:


RBAC

Column-Level Security

Masking


---

# 12. Future Readiness Requirements

The architecture shall support future adoption of:


Lakehouse Architecture

Apache Iceberg

Advanced ML Models

Real-Time AI Agents

Additional Data Sources


without significant redesign.

---

# Document Status

Version: 1.0

Status: APPROVED
