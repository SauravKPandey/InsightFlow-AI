# Decision Log

## Document Information

Version: 1.0

Status: Active

Owner: Architecture & Product Team

Last Updated: TBD

---

# Purpose

This document captures major business, product, architecture, and technology decisions made during the InsightFlow AI project.

A decision is considered finalized only after it has been recorded in this document.

---

## DEC-001

### Decision

Product name will be **InsightFlow AI**.

### Rationale

The name reflects the platform's ability to transform business events and operational data into actionable insights and intelligence.

### Alternatives Considered

* CB Insights (rejected)
* Other generic analytics platform names

### Status

Approved

---

## DEC-002

### Decision

Target domain will be **B2B SaaS organizations**.

### Rationale

B2B SaaS provides rich business scenarios involving subscriptions, renewals, churn, revenue intelligence, customer health, product adoption, and forecasting.

### Status

Approved

---

## DEC-003

### Decision

Initial cloud platform will be **Google Cloud Platform (GCP)**.

### Rationale

User has prior experience with GCP services and BigQuery. Future roadmap may include migration exercises to AWS.

### Status

Approved

---

## DEC-004

### Decision

Kafka will be used as the event streaming platform.

### Rationale

Kafka provides platform independence and supports future cloud portability.

### Alternatives Considered

* Google Pub/Sub

### Status

Approved

---

## DEC-005

### Decision

The platform will follow a simulated enterprise ecosystem architecture rather than a standalone SaaS application architecture.

### Rationale

Better reflects real-world enterprise environments where data originates from multiple systems.

### Source Systems

* CRM Service
* Billing Service
* Product Usage Service

### Status

Approved

---

## DEC-006

### Decision

Subscription billing frequencies will include:

* 1 Month
* 3 Months
* 6 Months
* 12 Months

### Rationale

Represents common SaaS billing models while providing sufficient complexity for analytics and forecasting.

### Status

Approved

---

## DEC-007

### Decision

Subscription lifecycle shall include a Grace Period state.

### Lifecycle States

* FREE
* TRIAL
* ACTIVE
* GRACE_PERIOD
* CANCELLED
* EXPIRED

### Rationale

Grace periods are common in subscription businesses and have direct revenue and retention implications.

### Status

Approved

---

## DEC-008

### Decision

Roadmap will follow a phased maturity model.

### Phases

1. Core Analytics Platform
2. Customer Intelligence
3. Predictive Intelligence
4. Natural Language Analytics
5. Knowledge Intelligence (RAG)
6. Agentic AI
7. Agentic AI-Powered Decision Intelligence

### Status

Approved

---

## DEC-009

### Decision

Predictive Intelligence will be implemented before RAG and Agentic AI.

### Rationale

Predictive analytics provides direct business value and depends on foundational data assets that are also required for future AI capabilities.

### Status

Approved

---

## DEC-010

### Decision

InsightFlow AI will prioritize business capabilities over technology features.

### Initial Capability Areas

* Revenue Intelligence
* Subscription Lifecycle Intelligence
* Product Adoption Intelligence
* Customer Health Intelligence
* Customer Retention Intelligence
* Executive Intelligence
* Predictive Intelligence
* Self-Service Analytics
* Business Alerting & Monitoring
* AI-Powered Insights

### Status

Approved

---

## DEC-011

### Decision

The platform roadmap shall incorporate enterprise-grade governance and security principles.

### Principles

* Security by Design
* Governance by Design
* Scalability by Design
* AI Responsibility
* Platform Agnosticism

### Governance Requirements

* RBAC
* Audit Logging
* Data Classification
* Data Lineage
* Encryption at Rest
* Encryption in Transit
* AI Explainability

### Status

Approved

---

## DEC-012

### Decision

Introduce a **Tenant** entity as the top-level business entity in the platform.

### Rationale

InsightFlow AI is designed for B2B SaaS organizations. The SaaS company using InsightFlow AI should be modeled separately from the customers it serves.

### Example

```text
Tenant = Salesforce

Customer Accounts:
- ABC Bank
- XYZ Insurance
```

### Status

Approved

---

## DEC-013

### Decision

Rename Customer entity to **Customer Account**.

### Rationale

A Customer Account represents an organization purchasing products from a Tenant and better reflects B2B SaaS terminology.

### Status

Approved

---

## DEC-014

### Decision

A Customer Account may subscribe to multiple products simultaneously.

### Rationale

Enterprise customers commonly purchase multiple products, enabling cross-sell analytics, product adoption analytics, expansion revenue tracking, and customer health scoring.

### Status

Approved

---

## DEC-015

### Decision

Revenue-related values shall not be stored on the Customer Account entity.

### Examples

```text
ARR
MRR
Contract Value
Customer Lifetime Value
```

### Rationale

These metrics shall be derived from Subscription and Payment data to maintain a single source of truth and avoid data inconsistencies.

### Status

Approved

---

## DEC-016

### Decision

Customer lifecycle shall support historical tracking through Start Date and End Date fields.

### Fields

```text
customer_start_date
customer_end_date
```

### Rationale

Supports historical reporting, cohort analysis, churn analysis, tenure calculations, and future SCD Type 2 implementation.

### Status

Approved

---

## DEC-017

### Decision

Introduce a separate **Product Category** entity.

### Rationale

Product Categories represent business groupings and enable portfolio-level reporting and analytics.

### Example

```text
Analytics
Marketing
Sales
Finance
```

### Status

Approved

---

## DEC-018

### Decision

A Product belongs to exactly one Product Category.

### Rationale

Ensures clear product classification and simplifies revenue, churn, and adoption reporting.

### Status

Approved

---

## DEC-019

### Decision

Separate Product and Plan into distinct entities.

### Rationale

Products and Plans represent different business concepts.

This enables:

* Revenue by Product
* Revenue by Plan
* Churn by Product
* Churn by Plan
* Pricing analytics

### Status

Approved

---

## DEC-020

### Decision

A Product can have multiple Plans.

### Example

```text
Analytics Cloud
├── FREE
├── STANDARD
├── PREMIUM
├── ENTERPRISE
└── CUSTOM
```

### Status

Approved

---

## DEC-021

### Decision

The initial Plan model will contain only a Plan Name attribute.

### Example

```text
FREE
STANDARD
PREMIUM
ENTERPRISE
CUSTOM
```

### Rationale

Keep the V1 model simple and intentionally allow future schema evolution to support more advanced enterprise pricing models.

### Future Evolution

Potential future fields:

```text
plan_type
plan_name
```

### Status

Approved

---

## DEC-022

### Decision

Future schema evolution will be treated as a learning objective for the project.

### Rationale

The project should intentionally provide opportunities to practice:

* Database migrations
* API versioning
* Kafka schema evolution
* Data model refactoring
* Backward compatibility

### Status

Approved

---

## DEC-023

### Decision

Customer Account segmentation shall include the following dimensions:

### Segmentation Dimensions

```text
Industry
Customer Size
Acquisition Channel
Country
Region
Customer Tier
```

### Rationale

These dimensions support executive reporting, churn analysis, revenue segmentation, forecasting, and customer health analytics.

### Status

Approved


-------------------------------

## DEC-024

### Decision
A Customer Account may have only one active subscription per Product.

### Example

Allowed:

```text
ABC Bank
    ↓
Analytics Cloud
    ↓
One Active Subscription
```

Not Allowed:

```text
ABC Bank
    ↓
Analytics Cloud
    ↓
Subscription A (ACTIVE)

ABC Bank
    ↓
Analytics Cloud
    ↓
Subscription B (ACTIVE)
```

### Rationale

Simplifies revenue analytics, churn calculations, forecasting, subscription lifecycle management, and customer reporting.

### Status

Approved

---

## DEC-025

### Decision

Subscription lifecycle statuses shall be:

```text
FREE
TRIAL
ACTIVE
GRACE_PERIOD
CANCELLED
EXPIRED
```

### Rationale

Represents realistic SaaS subscription journeys and supports churn, retention, revenue, and lifecycle analytics.

### Status

Approved

---

## DEC-026

### Decision

Subscription upgrades and downgrades shall update the existing subscription rather than create a new subscription.

### Rationale

Maintains subscription continuity and simplifies operational processing and reporting.

### Status

Approved

---

## DEC-027

### Decision

Subscription changes shall generate Kafka events and historical tracking shall be maintained in the analytics layer using SCD Type 2.

### Example Events

```text
subscription_created

subscription_renewed

subscription_upgraded

subscription_downgraded

subscription_cancelled

subscription_entered_grace_period

subscription_expired
```

### Rationale

Preserves historical context while keeping the operational model simple.

### Status

Approved

---

## DEC-028

### Decision

Subscription model shall support seat-based licensing.

### Field

```text
seat_count
```

### Rationale

Supports revenue analytics, product adoption analytics, customer health scoring, expansion revenue tracking, and churn prediction.

### Status

Approved

---

## DEC-029

### Decision

Subscription model shall store commercial contract values.

### Fields

```text
subscription_amount

currency
```

### Rationale

Represents contractual subscription value and supports revenue intelligence, forecasting, billing validation, and financial reporting.

### Status

Approved

---

## DEC-030

### Decision

A Subscription may have multiple Payments.

### Relationship

```text
Subscription
      ↓
Many Payments
```

### Rationale

Supports recurring billing cycles and payment retry scenarios.

### Status

Approved

---

## DEC-031

### Decision

Payment statuses shall be:

```text
SUCCESS

FAILED

REFUNDED
```

### Rationale

Provides sufficient payment lifecycle coverage for V1 while keeping the model simple.

### Status

Approved

---

## DEC-032

### Decision

Partial payments shall not be supported in V1.

### Rationale

Keeps the operational payment model simple and allows future schema evolution for more advanced billing scenarios.

### Status

Approved

---

## DEC-033

### Decision

Payment failures may trigger Grace Period workflows and eventual subscription expiry.

### Workflow

```text
Payment Failure
      ↓
Grace Period
      ↓
Subscription Expiry
```

### Rationale

Represents realistic SaaS subscription management and directly supports churn analytics.

### Status

Approved

---

## DEC-034

### Decision

A Customer Account may contain multiple Users.

### Relationship

```text
Customer Account
       ↓
Many Users
```

### Rationale

Supports enterprise SaaS user management and enables user-level adoption analytics.

### Status

Approved

---

## DEC-035

### Decision

User entity shall include organizational attributes.

### Attributes

```text
department

job_title

role
```

### Example Roles

```text
ADMIN

POWER_USER

STANDARD_USER
```

### Rationale

Supports product adoption analytics, customer health scoring, churn prediction, and future AI-driven insights.

### Status

Approved

---

## DEC-036

### Decision

Usage Events shall be captured at the feature level.

### Example Events

```text
LOGIN

DASHBOARD_VIEWED

REPORT_CREATED

FORECAST_GENERATED

EXPORT_DOWNLOADED

ALERT_CONFIGURED
```

### Rationale

Feature-level telemetry enables product adoption analytics, customer health scoring, feature adoption reporting, churn prediction, and Agentic AI capabilities.

### Status

Approved

---

## DEC-037

### Decision

Usage Events shall be immutable once generated.

### Rule

```text
Never Updated

Never Deleted
```

### Rationale

Aligns with event-driven architecture principles and Kafka event streaming best practices.

### Status

Approved

---

## DEC-038

### Decision

Usage Event entity shall support extensible event context through a metadata attribute.

### Field

```text
event_metadata
```

### Example

```json
{
  "report_type": "Revenue",
  "export_format": "PDF"
}
```

### Rationale

Provides flexibility for future feature enhancements without frequent schema changes.

### Status

Approved

---

## DEC-039

### Decision

The Business Entity Model v1.0 is approved and frozen.

### Approved Entities

```text
Tenant

Product Category

Product

Plan

Customer Account

Subscription

Payment

User

Usage Event
```

### Rationale

Provides the foundational business model required to support Revenue Intelligence, Subscription Lifecycle Intelligence, Product Adoption Intelligence, Customer Health Intelligence, Predictive Analytics, Natural Language Analytics, RAG, and Agentic AI capabilities.

### Status

Approved
------

DEC-040
Decision

KPI Definitions shall serve as the authoritative source for all business metric calculations across dashboards, reports, APIs, ML models, and AI capabilities.

Status

Approved

-----------------------------

## Business Entity Model Status:

### Frozen:
Tenant
Product Category
Product
Plan
Customer Account
Subscription
Payment
User
Usage Event



## Decision Logging Rules

A decision should be logged if it impacts:

* Business Scope
* Product Direction
* Architecture
* Technology Selection
* Security
* Governance
* Budget
* Delivery Approach

Minor implementation details do not require decision log entries.
