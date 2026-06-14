# 03_architectural_decisions.md

# Architectural Decision Record (ADR)

## Purpose

This document captures key architectural decisions made during the design of InsightFlow, including rationale, alternatives considered, and expected benefits.

---

# ADR-001: Adopt Medallion Architecture

Decision:


Landing → Bronze → Silver → Gold


Status:


Approved


Rationale:


Provides clear separation between raw, cleansed, and business-consumable data.
Widely adopted pattern for analytical platforms.


Alternatives Considered:


Single-Layer Warehouse
Data Vault


---

# ADR-002: Use BigQuery as Analytical Platform

Decision:


BigQuery


Status:


Approved


Rationale:


Serverless
Highly scalable
Native GCP integration
Strong SQL support


Alternatives Considered:


Snowflake
Redshift
Databricks SQL


---

# ADR-003: Use Kafka as Streaming Backbone

Decision:


Kafka


Status:


Approved


Rationale:


Decouples source systems from consumers.
Supports near real-time ingestion.
Industry standard event streaming platform.


---

# ADR-004: Archive Raw Data in GCS

Decision:


Kafka → GCS → Bronze


Status:


Approved


Rationale:


Replay capability
Audit support
Backfill support
Disaster recovery


---

# ADR-005: Bronze/Silver/Gold Implemented in BigQuery

Decision:


Bronze = BigQuery

Silver = BigQuery

Gold = BigQuery


Status:


Approved


Rationale:


Simplified architecture.
Reduced operational complexity.


---

# ADR-006: Defer Lakehouse Adoption

Decision:


No Iceberg / Delta / Hudi in v1


Status:


Approved


Rationale:


Current requirements do not justify additional complexity.
BigQuery satisfies analytical requirements.


---

# ADR-007: Silver as Canonical Business Layer

Decision:


Silver = Source of Truth


Status:


Approved


Rationale:


Provides a single trusted business layer.
Supports downstream reuse.


---

# ADR-008: Gold Contains Aggregates Only

Decision:


Gold = KPIs, Aggregates, Forecasts


Status:


Approved


Rationale:


Improved performance.
Simplified business consumption.


---

# ADR-009: Hybrid Entity-Based DAG Architecture

Decision:


One DAG per business entity.


Examples:


customer_pipeline_dag

subscription_pipeline_dag

payment_pipeline_dag


Status:


Approved


Rationale:


Improved ownership.
Simplified troubleshooting.
Easier backfills.


---

# ADR-010: Adopt SCD Type 2 for Historical Dimensions

Decision:


Customer

Subscription

Pricing Plan


Status:


Approved


Rationale:


Supports historical reporting.
Enables accurate point-in-time analysis.


---

# ADR-011: Retain Business Keys and Surrogate Keys

Decision:


Store both in fact tables.


Status:


Approved


Rationale:


Improves lineage.
Simplifies debugging.
Supports reconciliation.


---

# ADR-012: Use Unknown Member Strategy

Decision:


Surrogate Key = -1


Status:


Approved


Rationale:


Prevents pipeline failures due to missing dimensions.
Supports late arriving dimensions.


---

# ADR-013: Prioritize Data Availability

Decision:


Non-critical DQ failures do not stop pipelines.


Status:


Approved


Rationale:


Business users receive timely data.
Issues handled through monitoring and reconciliation.


---

# ADR-014: Metadata-Driven Processing

Decision:


Use metadata tables for orchestration and monitoring.


Status:


Approved


Rationale:


Improves observability.
Supports automation.


---

# ADR-015: Standardize Alerting Framework

Decision:


Email + Microsoft Teams


Status:


Approved


Rationale:


Simple operational model.
Easy integration with Airflow and monitoring tools.


---

# ADR-016: KPI-Driven Semantic Layer

Decision:


31 Approved KPIs


Status:


Approved


Rationale:


Provides a governed business metric framework.
Prevents KPI proliferation.


---

# Document Status

Version: 1.0

Status: APPROVED
