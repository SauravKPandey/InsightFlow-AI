# 04_high_level_design.md

## Document Information

**Project:** InsightFlow AI
**Version:** 1.0
**Status:** Approved & Frozen
**Document Owner:** Product & Engineering Team

---

# 1. Introduction

## Purpose

This document defines the high-level technical architecture for InsightFlow AI.

InsightFlow AI is an Agentic AI-powered Decision Intelligence platform designed for subscription-based businesses. The platform enables Revenue Intelligence, Subscription Lifecycle Intelligence, Product Adoption Intelligence, Customer Health Intelligence, Predictive Analytics, Natural Language Analytics, and AI-powered Decision Support.

---

# 2. Architecture Principles

### AP-001 Cloud Native

The platform shall leverage managed cloud services wherever possible.

### AP-002 API First

All platform capabilities shall be exposed through well-defined APIs.

### AP-003 Event Driven

Business events shall be captured and processed using an event-driven architecture.

### AP-004 Multi-Tenant by Design

The platform shall support multiple tenants using logical tenant isolation.

### AP-005 Security by Design

Security, governance, and compliance shall be embedded into every layer.

### AP-006 AI First

AI capabilities shall be integrated as first-class platform components.

### AP-007 Business Capability First

The architecture shall prioritize delivery of business capabilities over infrastructure sophistication until scale requirements justify additional complexity.

---

# 3. Solution Overview


Source Systems
      ↓
Kafka
      ↓
Python Consumer
      ↓
GCS Bronze
      ↓
DBT
      ↓
BigQuery Silver
      ↓
DBT
      ↓
BigQuery Gold
      ↓
Semantic Layer
      ↓
AI Platform
      ↓
FastAPI
      ↓
React UI
```

---

# 4. Logical Architecture


┌─────────────────────────────────────────┐
│             Source Systems              │
├─────────────────────────────────────────┤
│ CRM Systems                             │
│ Subscription Platforms                  │
│ Payment Systems                         │
│ Product Usage Events                    │
│ Application Telemetry                   │
└─────────────────────┬───────────────────┘
                      │
                      ▼

┌─────────────────────────────────────────┐
│              Kafka Topics               │
├─────────────────────────────────────────┤
│ customer-events                         │
│ subscription-events                     │
│ payment-events                          │
│ usage-events                            │
└─────────────────────┬───────────────────┘
                      │
                      ▼

┌─────────────────────────────────────────┐
│            Python Consumer              │
├─────────────────────────────────────────┤
│ Consume Events                          │
│ Basic Validation                        │
│ Error Handling                          │
│ Write Raw Events                        │
│ Processing Logs                         │
└─────────────────────┬───────────────────┘
                      │
                      ▼

┌─────────────────────────────────────────┐
│         Google Cloud Storage            │
│              Bronze Layer               │
└─────────────────────┬───────────────────┘
                      │
                      ▼

┌─────────────────────────────────────────┐
│                 DBT                     │
│         Bronze → Silver                 │
└─────────────────────┬───────────────────┘
                      │
                      ▼

┌─────────────────────────────────────────┐
│              BigQuery                   │
│             Silver Layer                │
└─────────────────────┬───────────────────┘
                      │
                      ▼

┌─────────────────────────────────────────┐
│                 DBT                     │
│          Silver → Gold                  │
└─────────────────────┬───────────────────┘
                      │
                      ▼

┌─────────────────────────────────────────┐
│              BigQuery                   │
│              Gold Layer                 │
└─────────────────────┬───────────────────┘
                      │
                      ▼

┌─────────────────────────────────────────┐
│            Semantic Layer               │
└─────────────────────┬───────────────────┘
                      │
                      ▼

┌─────────────────────────────────────────┐
│              AI Platform                │
└─────────────────────┬───────────────────┘
                      │
                      ▼

┌─────────────────────────────────────────┐
│             FastAPI APIs                │
└─────────────────────┬───────────────────┘
                      │
                      ▼

┌─────────────────────────────────────────┐
│         React Frontend UI               │
└─────────────────────────────────────────┘
```

---

# 5. Data Architecture

## Ingestion Layer

### Technology

* Kafka

### Topics

* customer-events
* subscription-events
* payment-events
* usage-events

### Processing Strategy

Python Consumers shall:

* Read Kafka events
* Perform basic validation
* Handle processing errors
* Write raw events to Bronze layer
* Generate ingestion logs

No business logic or KPI calculations shall be performed during ingestion.

---

## Bronze Layer

### Technology

Google Cloud Storage (GCS)

### Purpose

Store raw immutable source data.

### Storage Format

* JSON
* Parquet

### Example Structure


bronze/
├── customer/
├── subscription/
├── payment/
└── usage_event/
```

---

## Silver Layer

### Technology

BigQuery

### Purpose

Store cleaned and standardized business entities.

### Responsibilities

* Schema validation
* Deduplication
* Data standardization
* Data quality checks

### Example Tables


silver_customer
silver_subscription
silver_payment
silver_usage_event
```

---

## Gold Layer

### Technology

BigQuery

### Purpose

Business-ready analytical layer.

### Responsibilities

* KPI calculations
* Business transformations
* Customer health calculations
* Revenue intelligence
* Product adoption analytics

### Example Data Marts


gold_revenue
gold_customer_health
gold_product_adoption
gold_subscription_lifecycle
```

---

# 6. Semantic Layer

The semantic layer shall provide business abstraction over analytical tables.

### Example Metrics

* ARR
* MRR
* Churn Rate
* Customer Health Score
* Product Adoption Rate
* Revenue Growth %
* Forecasted Revenue

### Purpose

Provide a consistent business vocabulary for:

* Dashboards
* AI Agents
* Natural Language Analytics
* Executive Reporting

---

# 7. AI Architecture

InsightFlow AI shall consist of two independent knowledge systems.

---

## 7.1 Document Knowledge System

### Purpose

Answer business-definition and governance-related questions.

### Sources

* KPI Definitions
* BRD
* FRD
* HLD
* Decision Logs
* Business Glossary
* Product Documentation

### Pipeline


Documents
    ↓
Chunking
    ↓
Embeddings
    ↓
Vector Database
    ↓
RAG Retrieval
    ↓
LLM
```

### Vector Store

Phase 1:


pgvector
```

Future:


Vertex AI Vector Search
```

---

## 7.2 Analytics Knowledge System

### Purpose

Answer business analytics questions.

### Sources

* Gold Layer
* KPI Tables
* Revenue Tables
* Customer Health Tables
* Forecast Tables

### Pipeline


User Question
      ↓
Agent
      ↓
SQL Generation
      ↓
BigQuery
      ↓
Query Result
      ↓
LLM Explanation
```

---

# 8. Agent Architecture

## Agent Router

Responsible for routing user requests to the appropriate business agent.

---

## Revenue Intelligence Agent

Responsibilities:

* Revenue Analysis
* ARR Analysis
* MRR Analysis
* Revenue Forecasting

---

## Customer Health Agent

Responsibilities:

* Health Monitoring
* Churn Detection
* Retention Analysis

---

## Product Intelligence Agent

Responsibilities:

* Feature Adoption Analysis
* Product Usage Analysis
* Expansion Opportunity Identification

---

## Executive Intelligence Agent

Responsibilities:

* Executive Summaries
* Strategic Insights
* Business Recommendations

---

## Tool Layer

Agents shall access platform capabilities through tools.

### Supported Tools

* BigQuery Analytics Tool
* Document RAG Tool
* KPI Catalog Tool
* Business Rules Tool
* Forecasting Tool

---

# 9. API Architecture

## Technology

FastAPI

### API Domains


/api/v1/revenue
/api/v1/subscriptions
/api/v1/customer-health
/api/v1/adoption
/api/v1/predictions
/api/v1/chat
/api/v1/agents
```

---

# 10. Multi-Tenancy Strategy

## Approach

Shared Infrastructure with Logical Tenant Isolation.

### Tenant Key

Every business entity shall contain:


tenant_id
```

### Access Control

Users shall only access data belonging to their tenant.

### Future Support

Architecture shall support migration to dedicated tenant environments if required.

---

# 11. Security & Governance

## Identity & Access

* Role-Based Access Control (RBAC)

## Data Protection

* Encryption At Rest
* Encryption In Transit

## Governance

* Audit Logging
* Data Lineage
* AI Explainability

## Compliance Readiness

* GDPR Ready
* SOC2 Ready

---

# 12. Deployment Architecture

## Cloud Platform

Google Cloud Platform (GCP)

### Storage

* Google Cloud Storage

### Data Warehouse

* BigQuery

### Transformation

* DBT

### Orchestration

* Airflow

### Backend

* FastAPI
* Cloud Run

### Frontend

* React
* Cloud Run / Firebase Hosting

### AI

* OpenAI
* Vertex AI (Future)

### Secrets Management

* Google Secret Manager

### Monitoring

* Cloud Logging
* Cloud Monitoring

---

# 13. Scalability Strategy

## Phase 1


Kafka
GCS
BigQuery
DBT
FastAPI
OpenAI
```

---

## Phase 2


Caching Layer
Vector Search
Agent Orchestration
```

---

## Phase 3


Multi-Agent Workflows
Advanced Forecasting
Real-Time Insights
```

---

## Phase 4


Flink Evaluation
Lakehouse Evaluation
Real-Time Decision Intelligence
```

---

# 14. Future Architectural Enhancements

The following technologies are intentionally excluded from MVP and may be evaluated in future releases:

* Apache Flink
* Spark Structured Streaming
* Apache Iceberg
* Delta Lake
* Lakehouse Architecture
* Kafka Connect
* Dedicated Vector Databases
* Microservices Architecture

---

# 15. Technology Stack

| Layer             | Technology           |
| ----------------- | -------------------- |
| Frontend          | React + TypeScript   |
| Backend           | FastAPI              |
| Event Streaming   | Kafka                |
| Ingestion         | Python Consumer      |
| Data Lake         | Google Cloud Storage |
| Transformation    | DBT                  |
| Data Warehouse    | BigQuery             |
| Orchestration     | Airflow              |
| Vector Store      | pgvector             |
| LLM               | OpenAI               |
| Future LLM Option | Vertex AI            |
| Deployment        | Cloud Run            |
| Monitoring        | Cloud Monitoring     |
| Secrets           | Secret Manager       |

---

# 16. Architecture Decisions

### Approved Decisions

* Kafka for event ingestion
* Python Consumer for ingestion processing
* GCS Bronze Layer
* BigQuery Silver Layer
* BigQuery Gold Layer
* DBT Transformations
* Semantic Layer
* Dual Knowledge AI Architecture
* Agent-Based AI Design
* Shared Multi-Tenant Architecture
* FastAPI Backend
* React Frontend
* Cloud Run Deployment

### Deferred Decisions

* Apache Flink
* Lakehouse Architecture
* Iceberg / Delta Lake
* Microservices
* Dedicated Vector Search Platform

---

# Status

**Version:** 1.0
**Status:** Approved & Frozen
