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

----

## DEC-000

All approved business, architecture and data modeling decisions
shall be recorded in the Decision Log immediately upon approval.

Rationale:
Ensures traceability, prevents decision loss and maintains
consistency across project artifacts.

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


Analytics Cloud
├── FREE
├── STANDARD
├── PREMIUM
├── ENTERPRISE
└── CUSTOM
 ggg

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

job_titlef

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
------

DEC-041

AI Architecture shall consist of two independent knowledge systems:

1. Document Knowledge System
   - Powered by RAG and Vector Search
   - Used for business definitions, KPI definitions,
     architecture knowledge and governance.

2. Analytics Knowledge System
   - Powered by Semantic Layer and BigQuery
   - Used for KPI retrieval, trend analysis,
     forecasting and business insights.

Rationale:
Document retrieval and business analytics retrieval
represent different retrieval patterns and should be
architected independently.

status 

Approved
------

DEC-042

A customer account may have multiple active subscriptions simultaneously.

Each subscription shall be associated with a single product.

Rationale:
Enterprise customers commonly purchase multiple products
and maintain independent subscription lifecycles for each.

status 

Approved

-----------------------------

## Business Entity Model Status:

### Frozen:

Operational Entities
--------------------
Tenant
Customer
Product
Pricing Plan
Subscription
Invoice
Payment
User
Feature
Usage Event


Reference Entities
------------------
Country
Region
Customer Segment
Acquisition Channel
Product Category


Analytics Entity
--------------
Forecast

## Future entity

Support Ticket
Campaign
Partner

--------------

DEC-043

Title:
Primary Key Strategy for Dimensions and Fact Tables

Decision:
InsightFlow AI shall use surrogate keys for dimension tables and immutable business/event identifiers for fact tables.

Dimension Tables:
- dim_tenant        → tenant_key
- dim_customer      → customer_key
- dim_product       → product_key
- dim_subscription  → subscription_key
- dim_user          → user_key
- dim_feature       → feature_key
- dim_country       → country_key
- dim_region        → region_key
- dim_customer_segment → customer_segment_key
- dim_acquisition_channel → acquisition_channel_key

Fact Tables:
- fact_subscription_event → subscription_event_id
- fact_payment            → payment_id
- fact_invoice            → invoice_id
- fact_usage_event        → usage_event_id
- fact_forecast           → forecast_id

Fact Table Foreign Keys:
Fact tables shall reference dimension tables using surrogate keys.

Example:
fact_subscription_event
- subscription_event_id (PK)
- tenant_key (FK)
- customer_key (FK)
- product_key (FK)
- subscription_key (FK)

Rationale:
1. Surrogate keys are required to support SCD Type 2 dimensions.
2. Immutable business/event identifiers provide traceability back to source systems.
3. BigQuery does not require integer surrogate keys on fact tables for performance.
4. This approach simplifies debugging, lineage tracking, and event reconciliation.
5. The design aligns with modern cloud data warehouse practices while preserving dimensional modeling principles.

Status

Approved

---

DEC-044

Fact Table: fact_payment

Grain:
One row per payment attempt.

Business Rules:
1. An invoice may have multiple payment attempts.
2. An invoice may have multiple FAILED or PENDING payment attempts.
3. An invoice shall have at most one SUCCESSFUL payment.
4. Additional successful payments against the same invoice shall be treated as overpayments and handled through refund/reconciliation processes.
5. Refund transactions shall be stored in fact_payment as payment event types.

Rationale:
Supports payment retry analysis, revenue collection analysis, payment success rate calculations, and financial reconciliation while maintaining a complete payment history.

status 

Approved
---

DEC-045

Entity: Tenant

Decision:
Tenant shall contain industry as a business attribute.

Examples:
- SaaS
- FinTech
- Healthcare
- Retail
- Manufacturing

Rationale:
Industry-based benchmarking, adoption analysis, revenue analysis,
and future cross-tenant intelligence capabilities may require
tenant industry classification.

status

Approved
---

DEC-046

Entity: Customer Account

Decision:
Customer Tier shall be supported as a customer segmentation attribute.

Examples:
- Enterprise
- Mid-Market
- SMB

or

- Gold
- Silver
- Bronze

Rationale:
Customer tier is commonly used for segmentation,
reporting, customer success prioritization, churn analysis,
and forecasting.

Status 

Approved
---

DEC-047

Entity: Feature

Decision:
A Feature shall belong to exactly one Product.

Relationship:
Product (1) → (M) Feature

Rationale:
1. Simplifies product adoption analytics.
2. Simplifies feature adoption calculations.
3. Simplifies customer health scoring.
4. Simplifies dimensional modeling and reporting.
5. Shared features across products can be supported in future through a Product-Feature bridge table if required.

Status 

Approved
---

DEC-048

Entity: Feature

Decision:
Feature shall support a premium feature indicator.

Attribute:
feature_is_premium

Allowed Values:
TRUE
FALSE

Rationale:
1. Enables premium feature adoption analytics.
2. Supports expansion opportunity identification.
3. Supports customer health analysis.
4. Supports future product intelligence use cases.
5. Enables premium feature usage reporting and monetization analysis.

status

Approved
---

DEC-049

Entity: Subscription

Decision:
Subscription shall support both purchased seat count and assigned seat count.

Attributes:
- purchased_seat_count
- assigned_seat_count

Rationale:
1. Enables seat utilization analysis.
2. Supports customer health scoring.
3. Supports expansion opportunity identification.
4. Supports product adoption analysis.
5. Enables SaaS utilization KPIs.

Example:

Purchased Seats = 100
Assigned Seats = 60

Seat Utilization = 60%

Status

Approved
---

DEC-050

Entity: Invoice

Decision:
Invoice and Payment shall be modeled as separate business entities.

Invoice service period attributes shall not be included in MVP.


Relationship:
Invoice (1) → Payment (Many)


Implementation:
payment.invoice_id shall be used as the foreign key.


Excluded Attributes:
- invoice_period_start_date
- invoice_period_end_date

Rationale:

Supports multiple payment attempts per invoice.
Supports failed payment tracking.
Supports payment retry analytics.
Supports payment success rate calculations.
Aligns with standard relational modeling principles.
Current platform scope focuses on subscription analytics,
customer intelligence, forecasting and decision intelligence.

Revenue recognition and service period accounting are outside
the MVP scope and may be introduced in future releases if required.

status
Approved
---

DEC-051

Entity: Payment

Decision:
Payment shall support payment failure reason tracking.

Attribute:
failure_reason

Examples:
- INSUFFICIENT_FUNDS
- CARD_DECLINED
- NETWORK_ERROR
- GATEWAY_TIMEOUT
- FRAUD_CHECK_FAILED
- PAYMENT_CANCELLED

Rationale:
1. Enables payment failure analysis.
2. Supports payment retry optimization.
3. Supports payment intelligence dashboards.
4. Enables AI-driven payment insights.
5. Supports gateway performance analysis.

status
Approved
---

DEC-052

Entity: User

Decision:
User shall support role-based classification.

Attribute:
user_role

Examples:
- ADMIN
- POWER_USER
- STANDARD_USER
- READ_ONLY

Rationale:
1. Enables feature adoption analysis by user role.
2. Supports power user identification.
3. Supports customer health scoring.
4. Supports expansion opportunity analysis.
5. Provides additional signals for churn prediction models.

status

Approved
---
DEC-053

Entity: Usage Event

Decision:
Usage Event shall support a numeric event value.

Attribute:
event_value

Default Value:
1

Examples:

LOGIN
event_value = 1

API_CALLED
event_value = 500

EXPORT_COMPLETED
event_value = 25

Rationale:
1. Supports feature consumption analytics.
2. Supports API usage analysis.
3. Supports advanced product adoption metrics.
4. Enables future usage-based billing models.
5. Provides richer signals for customer health and AI models.

status

Approved
---

DEC-054

Entity: Pricing Plan

Decision:
Pricing shall be modeled as a separate business entity rather than as attributes on Product.

Relationship:
Product (1) → Pricing Plan (Many)
Pricing Plan (1) → Subscription (Many)

Rationale:
1. Supports multiple billing frequencies.
2. Supports seat-based pricing.
3. Supports historical price tracking.
4. Supports future pricing changes.
5. Preserves subscription pricing history.

status

Approved
---

DEC-055

Entities:
Pricing Plan
Subscription

Decision:
Pricing Plan shall store list pricing, while Subscription shall store contracted pricing.

Pricing Plan Attributes:
- base_price
- billing_frequency
- currency

Subscription Attributes:
- subscription_amount

Rationale:
1. Supports customer-specific negotiated pricing.
2. Supports enterprise discounting.
3. Supports grandfathered pricing.
4. Preserves contracted revenue values.
5. Supports accurate ARR and MRR calculations.
6. Prevents historical revenue changes when list prices are updated.

Example:

Pricing Plan:
Monthly Pro = $100/month

Customer A Subscription:
Contracted Price = $80/month

Customer B Subscription:
Contracted Price = $90/month 

status 
Approvedd
---

DEC-056

Entities:
Country
Region

Decision:
Country and Region shall be modeled as separate reference entities.

Relationship:
Region (1) → Country (Many)

Customer Account shall be associated with Country.

Region shall be derived through Country.

Rationale:
1. Prevents inconsistent geography assignments.
2. Eliminates duplicate region storage.
3. Simplifies maintenance of geographic hierarchies.
4. Supports standardized reporting across tenants.

Example:

APAC
 ├── India
 ├── Singapore
 └── Australia

Customer
    ↓
India
    ↓
APAC

status

Approved
---

DEC-057

Title:
SCD Strategy for Dimensions

Decision:
InsightFlow shall support Slowly Changing Dimension Type 2 (SCD2) for business dimensions where historical changes are analytically significant.

SCD2 Dimensions:
- dim_customer
- dim_pricing_plan
- dim_user
- dim_tenant

SCD1 Dimensions:
- dim_product
- dim_feature
- dim_customer_segment

SCD0 Dimensions:
- dim_country
- dim_region
- dim_acquisition_channel
- dim_date

Rationale:
1. Preserves historical business context.
2. Enables customer journey analytics.
3. Supports expansion and churn analysis.
4. Supports AI/ML feature generation.
5. Preserves historical revenue attribution.

status
Approved
---

DEC-058

Entity:
dim_customer

Decision:
Country and Region attributes shall be denormalized into dim_customer.

Attributes:
- country_key
- country_name
- region_key
- region_name

Rationale:
1. Simplifies analytical queries.
2. Reduces joins.
3. Aligns with dimensional modeling principles.
4. Improves BI reporting performance.
5. Supports common geographic aggregations.

status 
Aoorived
---
DEC-059

Entity:
dim_subscription

Decision:
Subscription shall be modeled as a Slowly Changing Dimension Type 2 (SCD2).

Rationale:
1. Subscription attributes change over time.
2. Supports upgrade and downgrade analysis.
3. Supports historical ARR and MRR calculations.
4. Supports churn and renewal analytics.
5. Supports expansion and contraction revenue tracking.

Tracked Attributes:
- subscription_status
- subscription_amount
- purchased_seat_count
- assigned_seat_count
- auto_renew_flag
- pricing_plan

status:
Approved
----

DEC-060

Entity:
dim_subscription

Decision:
Contracted subscription pricing shall be stored in dim_subscription.

Attribute:
subscription_amount

Rationale:
1. Supports negotiated pricing.
2. Supports customer-specific discounts.
3. Supports grandfathered contracts.
4. Preserves historical contract value.
5. Pricing Plan stores list price while Subscription stores contracted price.

Example:

Pricing Plan:
Annual Pro = ₹100,000

Customer A Subscription:
₹85,000

Customer B Subscription:
₹90,000

status
Approved
---

DEC-061

Entity:
dim_product

Decision:
Product Category shall be stored directly within dim_product.

Attributes:
- product_category_id
- product_category_name

Rationale:
1. Product Category is small and relatively static.
2. Product and Product Category are almost always analyzed together.
3. Reduces joins in analytical queries.
4. Aligns with Kimball dimensional modeling principles.
5. Improves dashboard performance and usability.

status
Approved
---

DEC-062

Entity:
dim_pricing_plan

Decision:
Pricing Plan shall be modeled as a Slowly Changing Dimension Type 2 (SCD2).

Rationale:
1. Preserves pricing history.
2. Supports historical ARR and MRR calculations.
3. Supports pricing effectiveness analysis.
4. Supports forecasting and trend analysis.
5. Prevents historical financial metrics from changing when list prices are updated.

Example:

Annual Pro
2026 = ₹100,000

Annual Pro
2027 = ₹120,000

c
-----
DEC-063

Entity:
dim_user

Decision:
User shall maintain a direct relationship to Customer.

Attribute:
customer_key

Rationale:
1. Simplifies customer-level adoption analytics.
2. Simplifies DAU and MAU calculations.
3. Supports customer health scoring.
4. Supports power-user identification.
5. Reduces query complexity for user-centric analytics.

status
Approved
---
DEC-064

Entity:
dim_feature

Decision:
Feature shall be modeled as a Slowly Changing Dimension Type 1 (SCD1).

Rationale:
1. Feature attributes are primarily metadata.
2. Historical feature metadata is not required for approved KPIs.
3. Simplifies dimension maintenance.
4. Reduces storage and ETL complexity.
5. Feature usage history is already preserved in fact_usage_event.

status
Approved
----
DEC-065

Forecast removed as core business entity.

Reason:
Forecast is an analytical artifact generated from business data,
not an operational business entity.

Future analytical artifacts may include:
- Forecast
- Customer Health Score
- Churn Prediction
- Recommendations
-------------

DEC-066

Title:
Subscription Events Processing Layer

Decision:
A dedicated silver_subscription_event table shall be introduced.

Flow:

source_events
      +
derived_events
      ↓
silver_subscription_event
      ↓
fact_subscription_event

Rationale:
1. Maintains Bronze → Silver → Gold architecture consistency.
2. Separates business event derivation from analytics consumption.
3. Allows event validation and enrichment before Gold.
4. Supports both source-generated and warehouse-derived events.
5. Simplifies troubleshooting and reconciliation.

---
DEC-067

Title:
Silver as Canonical Business Layer

Decision:

Dimensions and Facts shall reside in Silver.

Gold shall contain only business-consumption artifacts.

Silver:
- Dimensions
- Facts
- Trusted Business Data

Gold:
- KPI Tables
- Aggregate Tables
- AI Feature Tables
- Forecast Outputs
- Recommendation Outputs

Rationale:

1. Establishes Silver as the Single Source of Truth.
2. Aligns with modern Lakehouse architecture patterns.
3. Supports BI, Data Science, AI, and GenAI from a common business layer.
4. Separates business facts from derived business insights.
5. Improves scalability for future AI and forecasting use cases.

---
# Section 5: Physical Data Model

## Purpose

This section defines the physical implementation standards for InsightFlow on GCP. It establishes dataset organization, naming conventions, datatype standards, key generation strategy, SCD implementation, partitioning, clustering, incremental loading, and metadata management.

---

# 5.1 Physical Architecture Principles

## Principle 1: Business First, Technology Second

The physical implementation shall follow the approved:

* Conceptual Model
* Logical Model
* Dimensional Model

Technology choices must support the business model rather than drive it.

---

## Principle 2: Single Source of Truth

The Silver layer shall serve as the canonical business layer.

All dimensions and facts shall reside in Silver.

---

## Principle 3: Gold Contains Business Intelligence

Gold shall contain only:

* KPI tables
* Aggregate tables
* AI feature tables
* Forecast outputs
* Recommendation outputs

Raw operational transactions shall not be stored in Gold.

---

## Principle 4: Schema Evolution Friendly

The architecture must support:

* New entities
* New attributes
* New event types
* New KPIs

without major redesign.

---

## Principle 5: Cloud-Native Design

The solution shall be optimized for:

* BigQuery
* GCS
* Kafka
* Airflow / Cloud Composer
* Dataproc (if required)

---

# 5.2 Dataset Design

The platform shall use five primary datasets.

## Landing

Purpose:

Temporary ingestion layer.

Examples:

```text
landing.customer
landing.subscription
landing.payment
```

---

## Bronze

Purpose:

Persistent raw storage.

Examples:

```text
bronze.customer
bronze.subscription
bronze.invoice
bronze.payment
```

---

## Silver

Purpose:

Canonical business layer.

Examples:

```text
silver.dim_customer
silver.dim_subscription

silver.fact_invoice
silver.fact_payment
```

---

## Gold

Purpose:

Business intelligence and AI layer.

Examples:

```text
gold.agg_daily_arr
gold.customer_health_score
gold.forecast_revenue
```

---

## Metadata

Purpose:

Operational control and monitoring.

Examples:

```text
metadata.pipeline_run
metadata.pipeline_watermark
metadata.data_quality_results
```

---

# 5.3 Naming Standards

## Dataset Naming

All dataset names shall be:

* Lowercase
* Singular

Examples:

```text
landing
bronze
silver
gold
metadata
```

---

## Bronze Tables

Pattern:

```text
<entity_name>
```

Examples:

```text
customer
subscription
invoice
payment
```

---

## Silver Dimensions

Pattern:

```text
dim_<entity>
```

Examples:

```text
dim_customer
dim_subscription
dim_product
```

---

## Silver Facts

Pattern:

```text
fact_<business_event>
```

Examples:

```text
fact_payment
fact_invoice
fact_usage_event
fact_subscription_event
```

---

## Gold Aggregates

Pattern:

```text
agg_<metric>
```

Examples:

```text
agg_daily_arr
agg_monthly_revenue
```

---

## Gold Feature Tables

Pattern:

```text
feature_<business_feature>
```

Examples:

```text
feature_customer_health
feature_churn_prediction
```

---

## Gold Forecast Tables

Pattern:

```text
forecast_<metric>
```

Examples:

```text
forecast_revenue
forecast_arr
```

---

## Column Naming

All column names shall use:

```text
snake_case
```

Examples:

```text
customer_id
customer_name
payment_amount
event_timestamp
```

---

## Key Naming

Business Keys:

```text
customer_id
subscription_id
invoice_id
payment_id
```

Surrogate Keys:

```text
customer_key
subscription_key
product_key
pricing_plan_key
```

---

# 5.4 Data Type Standards

| Category        | Data Type |
| --------------- | --------- |
| Business Keys   | STRING    |
| Surrogate Keys  | INT64     |
| Currency Values | NUMERIC   |
| Counts          | INT64     |
| Dates           | DATE      |
| Timestamps      | TIMESTAMP |
| Flags           | BOOLEAN   |
| Status Values   | STRING    |
| Raw Payloads    | JSON      |

---

## Timestamp Standard

All timestamps shall be stored in:

```text
UTC
```

---

# 5.5 Surrogate Key Strategy

## Standard

Business Keys:

```text
STRING
```

Surrogate Keys:

```text
INT64
```

---

## Generation Method

Metadata-driven sequence generation.

Control table:

```text
metadata.key_sequence
```

Example:

| entity_name  | last_key_value |
| ------------ | -------------- |
| customer     | 1050           |
| subscription | 890            |

---

## Unknown Member

Every dimension shall contain:

| surrogate_key | business_key |
| ------------- | ------------ |
| -1            | UNKNOWN      |

Used for:

* Late arriving dimensions
* Data quality issues
* Reconciliation scenarios

---

# 5.6 SCD2 Implementation Strategy

## SCD2 Dimensions

```text
dim_customer

dim_subscription

dim_pricing_plan

dim_user
```

---

## SCD1 Dimensions

```text
dim_product

dim_feature

dim_country

dim_region

dim_customer_segment

dim_acquisition_channel
```

---

## Standard SCD2 Columns

```text
effective_from_date

effective_to_date

is_current
```

---

## Open End Date

Current record:

```text
effective_to_date = 9999-12-31
```

---

## Current Record Identification

```text
is_current = TRUE
```

---

## Fact Resolution Rule

Facts shall resolve dimensions during load using:

```text
business_key
+
event_date
```

and store the corresponding surrogate key.

---

## Fact Lineage Standard

Fact tables shall retain both:

```text
surrogate_key
```

and

```text
business_key
```

Example:

```text
customer_key
customer_id

subscription_key
subscription_id
```

This supports:

* Historical accuracy
* Reconciliation
* Debugging
* Lineage

---

# 5.7 Partitioning Standards

## Partitioned Fact Tables

### fact_usage_event

Partition:

```text
event_timestamp
```

Granularity:

```text
DAY
```

---

### fact_payment

Partition:

```text
payment_processed_timestamp
```

Granularity:

```text
DAY
```

---

### fact_subscription_event

Partition:

```text
event_timestamp
```

Granularity:

```text
DAY
```

---

### fact_invoice

Partition:

```text
invoice_date
```

Granularity:

```text
MONTH
```

---

## Dimensions

No partitioning initially.

---

# 5.8 Clustering Standards

## fact_usage_event

Cluster by:

```text
customer_key
user_key
feature_key
```

---

## fact_payment

Cluster by:

```text
customer_key
subscription_key
```

---

## fact_invoice

Cluster by:

```text
customer_key
subscription_key
```

---

## fact_subscription_event

Cluster by:

```text
customer_key
subscription_key
```

---

## Dimensions

No clustering initially.

---

# 5.9 Incremental Load Strategy

## Streaming Sources

Primary mechanism:

```text
Kafka
```

Examples:

```text
Usage Events

Customer Change Events

Subscription Events
```

---

## Batch Sources

Examples:

```text
Invoices

Payments

Reference Data

MDM Data
```

---

## Preferred Loading Strategy

### Tier 1

CDC (Preferred)

Examples:

```text
Customer

Subscription
```

---

### Tier 2

Timestamp-Based Incremental

Pattern:

```sql
WHERE updated_timestamp > watermark
```

---

### Tier 3

Snapshot Comparison

Used only when CDC and timestamps are unavailable.

---

## Watermark Management

Control table:

```text
metadata.pipeline_watermark
```

Example:

| pipeline_name | last_successful_timestamp |
| ------------- | ------------------------- |
| customer_load | 2026-07-10 10:00          |

---

## Reprocessing Support

All pipelines shall support:

```text
start_date

end_date
```

parameters.

---

## Late Arriving Dimensions

Unknown dimensions shall be loaded using:

```text
surrogate_key = -1
```

and reconciled through scheduled correction jobs.

---

# 5.10 Metadata & Audit Framework

## Metadata Dataset

```text
metadata
```

---

## metadata.pipeline_run

Tracks pipeline execution history.

Key attributes:

```text
run_id
pipeline_name
start_timestamp
end_timestamp
status
records_processed
records_failed
error_message
```

---

## metadata.pipeline_watermark

Tracks incremental load progress.

Key attributes:

```text
pipeline_name
last_successful_timestamp
```

---

## metadata.data_quality_results

Tracks DQ validation results.

Key attributes:

```text
run_id
table_name
check_name
check_status
failed_record_count
execution_timestamp
```

---

## metadata.reconciliation_summary

Tracks unresolved dimensions.

Key attributes:

```text
table_name
unknown_dimension
record_count
execution_timestamp
```

---

## Audit Columns

### Dimensions

Mandatory:

```text
created_timestamp

updated_timestamp

source_system
```

---

### Facts

Mandatory:

```text
event_timestamp

created_timestamp

source_system
```

---

## Error Handling Standard

Missing dimensions shall not fail pipelines.

Instead:

```text
surrogate_key = -1
```

shall be assigned and the issue logged for reconciliation.

---

## Operational Monitoring KPIs

The platform shall monitor:

```text
Pipeline Success %

Pipeline Duration

Records Loaded

Records Failed

Unknown Dimension %

Data Freshness
```

---

# Section Status

Section 5: Physical Data Model

Status: APPROVED AND FROZEN

Version: 1.0
---



## Decision Logging Rules

A decision should be logged if it impacts:s

* Business Scope
* Product Direction
* Architecture
* Technology Selection
* Security
* Governance
* Budget
* Delivery Approach
Minor implementation details do not require decision log entries.
