# 15_data_model.md

## Section 1: Conceptual Data Model

### Purpose

The Conceptual Data Model defines the core business entities managed by InsightFlow AI and the relationships between those entities.

The conceptual model is technology agnostic and serves as the foundation for the logical, dimensional, and physical data models.

The conceptual model captures:

* Business entities
* Business relationships

The conceptual model intentionally excludes:

* Attributes
* Primary keys
* Foreign keys
* Data types
* Fact tables
* Dimension tables
* SCD strategies
* Physical storage considerations

---

# Approved Business Entities

## Operational Entities

### Tenant

Represents an organization using InsightFlow AI.

---

### Customer Account

Represents a customer purchasing products or services from a tenant.

---

### Subscription

Represents a commercial agreement between a customer and a tenant for a specific product.

A customer may maintain multiple active subscriptions simultaneously.

Each subscription is associated with a single product.

---

### Invoice

Represents a bill generated for a subscription.

---

### Payment

Represents a payment attempt against an invoice.

Multiple payment attempts may exist for a single invoice.

---

### Product

Represents a sellable offering.

---

### User

Represents a named user associated with a customer account.

---

### Feature

Represents a product capability available to users.

---

### Usage Event

Represents an interaction between a user and a feature.

---

## Reference Entities

### Product Category

Represents the category to which a product belongs.

---

### Customer Segment

Represents customer classification used for business analysis and segmentation.

Examples include:

* Industry
* Customer Size

---

### Acquisition Channel

Represents the channel through which a customer was acquired.

Examples include:

* Direct Sales
* Referral
* Partner
* Digital Marketing
* Organic

---

### Country

Represents customer geography.

---

### Region

Represents geographical grouping of countries.

---


---

# Business Relationships

## Tenant Relationships

A Tenant may have:

* Multiple Customer Accounts
* Multiple Products
* Multiple Forecasts

---

## Customer Relationships

A Customer Account may have:

* Multiple Subscriptions
* Multiple Users

A Customer Account is associated with:

* A Customer Segment
* An Acquisition Channel
* A Country
* A Region

---

## Subscription Relationships

A Subscription:

* Belongs to a Customer Account
* Is associated with a Product
* May generate multiple Invoices

---

## Invoice Relationships

An Invoice:

* Belongs to a Subscription
* May have multiple Payment Attempts

---

## Payment Relationships

A Payment:

* Belongs to an Invoice

---

## Product Relationships

A Product:

* Belongs to a Product Category
* May contain multiple Features

---

## Usage Relationships

A User:

* May generate multiple Usage Events

A Usage Event:

* References a Feature

---

# Conceptual Relationship Diagram

Tenant
│
├── Customer Account
│      │
│      ├── Subscription
│      │       │
│      │       ├── Invoice
│      │       │      │
│      │       │      └── Payment
│      │       │
│      │       └── Product
│      │
│      ├── User
│      │      │
│      │      └── Usage Event
│      │               │
│      │               └── Feature
│      │
│      ├── Customer Segment
│      ├── Acquisition Channel
│      ├── Country
│      └── Region
│
├── Product
│      │
│      ├── Product Category
│      └── Feature
│
└── Forecast

---

# Conceptual Model Status

Version: 1.0

Status: Approved & Frozen

Notes:

* Customer may have multiple active subscriptions.
* Invoice and Payment are separate business entities.
* Multiple payment attempts are allowed.
* Forecast is treated as an analytical entity.
* Detailed attributes, keys, dimensional modeling, and SCD strategies will be defined in subsequent sections of this document.

# Section 2: Logical Data Model

## Purpose

The Logical Data Model defines the business entities, attributes, business keys, and relationships required to support InsightFlow AI.

The logical model serves as the bridge between the Conceptual Data Model and the Dimensional Data Model.

The logical model includes:

* Business entities
* Business attributes
* Business keys
* Entity relationships

The logical model intentionally excludes:

* Surrogate keys
* Fact tables
* Dimension tables
* Physical storage design
* Data types
* Partitioning strategies
* SCD strategies

---

# Operational Entities

## Tenant

### Business Description

Represents an organization using InsightFlow AI.

A tenant owns customers, products, subscriptions, usage data, and forecasts.

### Business Key


tenant_id


### Attributes


tenant_id
tenant_name
tenant_status
industry
website
tenant_start_date
tenant_end_date
created_timestamp
updated_timestampc


### Relationships


Tenant
│
├── Customer Account
├── Product
├── Subscription
├── User
└── Forecast


---

## Customer Account

### Business Description

Represents a customer purchasing products or services from a tenant.

A customer may maintain multiple active subscriptions.

### Business Key


customer_id


### Attributes


customer_id
customer_name
customer_status

industry
customer_size
customer_tier

customer_start_date
customer_end_date

created_timestamp
updated_timestamp


### Relationships


Customer Account
│
├── Subscription
├── User
├── Customer Segment
├── Acquisition Channel
└── Country


---

## Product

### Business Description

Represents a sellable offering provided by a tenant.

A product may contain multiple features.

A product belongs to a single product category.

### Business Key


product_id


### Attributes


product_id
product_name
product_description
product_status

product_launch_date
product_retirement_date

created_timestamp
updated_timestamp


### Relationships


Product
│
├── Product Category
├── Pricing Plan
├── Feature
└── Subscription


---

## Pricing Plan

### Business Description

Represents a commercial pricing configuration for a product.

Pricing Plans define the commercial terms under which subscriptions are sold.

### Business Key


pricing_plan_id


### Attributes


pricing_plan_id
pricing_plan_name
pricing_plan_status

base_price
currency
billing_frequency

minimum_seats
maximum_seats

effective_start_date
effective_end_date

created_timestamp
updated_timestamp


### Relationships


Pricing Plan
│
├── Product
└── Subscription


---

## Feature

### Business Description

Represents a capability or functionality offered within a product.

Users interact with features through usage events.

### Business Key


feature_id


### Attributes


feature_id
feature_name
feature_description
feature_status

feature_type
feature_is_premium

feature_launch_date
feature_retirement_date

created_timestamp
updated_timestamp


### Relationships


Feature
│
├── Product
└── Usage Event


---

## Subscription

### Business Description

Represents a commercial agreement between a customer and a product.

A customer may maintain multiple active subscriptions simultaneously.

Each subscription is associated with a single pricing plan.

### Business Key


subscription_id


### Attributes


subscription_id
subscription_name
subscription_status

subscription_amount

purchased_seat_count
assigned_seat_count

subscription_start_date
subscription_end_date
grace_period_end_date

auto_renew_flag

created_timestamp
updated_timestamp


### Relationships


Subscription
│
├── Customer Account
├── Product
├── Pricing Plan
└── Invoice


---

## Invoice

### Business Description

Represents a bill generated against a subscription.

An invoice may have multiple payment attempts.

### Business Key


invoice_id


### Attributes


invoice_id
invoice_number
invoice_status

invoice_amount
tax_amount
discount_amount
net_amount

currency

invoice_date
due_date
paid_date

created_timestamp
updated_timestamp


### Relationships


Invoice
│
├── Subscription
└── Payment


---

## Payment

### Business Description

Represents a payment attempt against an invoice.

Multiple payment attempts may exist for a single invoice.

### Business Key


payment_id


### Attributes


payment_id

payment_status
payment_method

payment_amount
currency

payment_gateway
gateway_transaction_id

failure_reason

payment_attempt_timestamp
payment_processed_timestamp

created_timestamp
updated_timestamp


### Relationships


Payment
│
└── Invoice


---

## User

### Business Description

Represents a named user belonging to a customer account.

Users consume seats and generate usage activity.

### Business Key


user_id


### Attributes


user_id
user_name
email

user_status
user_role

is_seat_assigned

user_activation_date
user_deactivation_date

last_login_timestamp

created_timestamp
updated_timestamp


### Relationships


User
│
├── Customer Account
└── Usage Event


---

## Usage Event

### Business Description

Represents a user interaction with a product feature.

Usage Events form the foundation of product analytics, adoption analytics, customer health, and AI insights.

### Business Key


usage_event_id


### Attributes


usage_event_id

event_type
event_value

event_timestamp

session_id

device_type
platform

user_id
feature_id

created_timestamp


### Relationships


Usage Event
│
├── User
└── Feature


---

# Reference Entities

## Product Category

### Business Key


product_category_id


### Attributes


product_category_id
product_category_name
product_category_description
product_category_status

created_timestamp
updated_timestamp


---

## Customer Segment

### Business Key


customer_segment_id


### Attributes


customer_segment_id
customer_segment_name
customer_segment_description
customer_segment_status

created_timestamp
updated_timestamp


---

## Acquisition Channel

### Business Key


acquisition_channel_id


### Attributes


acquisition_channel_id
acquisition_channel_name
acquisition_channel_description
acquisition_channel_status

created_timestamp
updated_timestamp


---

## Region

### Business Key


region_id


### Attributes


region_id
region_name
region_description

created_timestamp
updated_timestamp


---

## Country

### Business Key


country_code


### Attributes


country_code
country_name

created_timestamp
updated_timestamp


### Relationships


Region (1) → Country (Many)


---




---

# Logical Data Model Status

Version: 1.0

Status: Approved & Frozen

# Section 3: Dimensional Data Model

## Purpose

The Dimensional Data Model provides an analytics-optimized representation of business data for reporting, KPI computation, forecasting, customer intelligence, and AI-driven insights.

The dimensional model follows a hybrid Kimball approach using:

* Dimensions for business entities and descriptive attributes
* Facts for business events and measurable activities
* Surrogate Keys for all dimensions
* SCD strategies based on business requirements

---

# Dimension Inventory

| Dimension               | Business Key           | Surrogate Key           | SCD Type |
| ----------------------- | ---------------------- | ----------------------- | -------- |
| dim_tenant              | tenant_id              | tenant_key              | SCD2     |
| dim_customer            | customer_id            | customer_key            | SCD2     |
| dim_subscription        | subscription_id        | subscription_key        | SCD2     |
| dim_product             | product_id             | product_key             | SCD1     |
| dim_pricing_plan        | pricing_plan_id        | pricing_plan_key        | SCD2     |
| dim_feature             | feature_id             | feature_key             | SCD1     |
| dim_user                | user_id                | user_key                | SCD2     |
| dim_country             | country_code           | country_key             | SCD0     |
| dim_region              | region_id              | region_key              | SCD0     |
| dim_customer_segment    | customer_segment_id    | customer_segment_key    | SCD1     |
| dim_acquisition_channel | acquisition_channel_id | acquisition_channel_key | SCD0     |


---

# dim_tenant

## Purpose

Stores tenant metadata and historical tenant changes.

## Keys


tenant_key (SK)
tenant_id (BK)


## SCD Strategy


SCD Type 2


## Attributes


tenant_key
tenant_id

tenant_name
tenant_status

industry
website

tenant_start_date
tenant_end_date

effective_from_date
effective_to_date

is_current

created_timestamp
updated_timestamp


---

# dim_customer

## Purpose

Stores customer metadata and historical customer changes.

Supports customer intelligence, churn analytics, forecasting, and customer health.

## Keys


customer_key (SK)
customer_id (BK)


## SCD Strategy


SCD Type 2


## Attributes


customer_key
customer_id

customer_name
customer_status

industry
customer_size
customer_tier

country_key
country_name

region_key
region_name

acquisition_channel_key
customer_segment_key

customer_start_date
customer_end_date

effective_from_date
effective_to_date

is_current

created_timestamp
updated_timestamp


---

# dim_subscription

## Purpose

Stores historical subscription state.

Supports ARR, MRR, renewals, churn, expansion, contraction, forecasting, and seat utilization analytics.

## Keys


subscription_key (SK)
subscription_id (BK)


## SCD Strategy


SCD Type 2


## Attributes


subscription_key
subscription_id

customer_key
product_key
pricing_plan_key

subscription_name
subscription_status

subscription_amount

purchased_seat_count
assigned_seat_count

auto_renew_flag

subscription_start_date
subscription_end_date

grace_period_end_date

effective_from_date
effective_to_date

is_current

created_timestamp
updated_timestamp


---

# dim_product

## Purpose

Stores product metadata.

## Keys


product_key (SK)
product_id (BK)


## SCD Strategy


SCD Type 1


## Attributes


product_key
product_id

product_name
product_description
product_status

product_category_id
product_category_name

product_launch_date
product_retirement_date

created_timestamp
updated_timestamp


---

# dim_pricing_plan

## Purpose

Stores pricing plan metadata and historical pricing changes.

Supports ARR, MRR, pricing analytics, forecasting, and revenue intelligence.

## Keys


pricing_plan_key (SK)
pricing_plan_id (BK)


## SCD Strategy


SCD Type 2


## Attributes


pricing_plan_key
pricing_plan_id

product_key

pricing_plan_name

base_price
currency

billing_frequency

minimum_seats
maximum_seats

pricing_plan_status

effective_from_date
effective_to_date

is_current

created_timestamp
updated_timestamp


---

# dim_feature

## Purpose

Stores product feature metadata.

Supports feature adoption analytics and product intelligence.

## Keys


feature_key (SK)
feature_id (BK)


## SCD Strategy


SCD Type 1


## Attributes


feature_key
feature_id

product_key

feature_name
feature_description

feature_type
feature_status

feature_is_premium

feature_launch_date
feature_retirement_date

created_timestamp
updated_timestamp


---

# dim_user

## Purpose

Stores user metadata and historical user changes.

Supports DAU, MAU, adoption analytics, customer health, and churn prediction.

## Keys


user_key (SK)
user_id (BK)


## SCD Strategy


SCD Type 2


## Attributes


user_key
user_id

customer_key

user_name
email

user_role
user_status

is_seat_assigned

user_activation_date
user_deactivation_date

last_login_timestamp

effective_from_date
effective_to_date

is_current

created_timestamp
updated_timestamp


---

# dim_country

## Keys


country_key (SK)
country_code (BK)


## SCD Strategy


SCD Type 0


## Attributes


country_key
country_code

country_name

created_timestamp
updated_timestamp


---

# dim_region

## Keys


region_key (SK)
region_id (BK)


## SCD Strategy


SCD Type 0


## Attributes


region_key
region_id

region_name
region_description

created_timestamp
updated_timestamp


---

# dim_customer_segment

## Keys


customer_segment_key (SK)
customer_segment_id (BK)


## SCD Strategy


SCD Type 1


## Attributes


customer_segment_key
customer_segment_id

customer_segment_name
customer_segment_description
customer_segment_status

created_timestamp
updated_timestamp


---

# dim_acquisition_channel

## Keys


acquisition_channel_key (SK)
acquisition_channel_id (BK)


## SCD Strategy


SCD Type 0


## Attributes


acquisition_channel_key
acquisition_channel_id

acquisition_channel_name
acquisition_channel_description
acquisition_channel_status

created_timestamp
updated_timestamp


---

# Fact Tables

## Fact Inventory

| Fact Table              | Purpose                              |
| ----------------------- | ------------------------------------ |
| fact_subscription_event | Subscription lifecycle analytics     |
| fact_invoice            | Billing and invoicing analytics      |
| fact_payment            | Payment and collections analytics    |
| fact_usage_event        | Product usage and adoption analytics |

---

# fact_subscription_event

## Purpose

Captures all subscription lifecycle events.

Supports:

* ARR
* MRR
* Net Revenue Retention (NRR)
* Gross Revenue Retention (GRR)
* Expansion Revenue
* Contraction Revenue
* Renewals
* Churn
* Forecasting

## Grain

One row per subscription lifecycle event.

## Primary Key


subscription_event_id


## Foreign Keys


tenant_key

customer_key

subscription_key

product_key

pricing_plan_key


## Event Attributes


event_type

event_timestamp

event_source


Allowed Event Types:


SUBSCRIPTION_CREATED

SUBSCRIPTION_ACTIVATED

SUBSCRIPTION_RENEWED

PLAN_UPGRADED

PLAN_DOWNGRADED

SEATS_INCREASED

SEATS_DECREASED

AUTO_RENEW_ENABLED

AUTO_RENEW_DISABLED

SUBSCRIPTION_CANCELLED

SUBSCRIPTION_EXPIRED

GRACE_PERIOD_STARTED

GRACE_PERIOD_ENDED


## Measures


event_amount_delta

event_seat_delta


Examples:

| Event     | Amount Delta | Seat Delta |
| --------- | ------------ | ---------- |
| Created   | +120000      | +100       |
| Upgrade   | +60000       | +50        |
| Downgrade | -30000       | -25        |
| Cancelled | -180000      | -150       |

## Audit


created_timestamp


---

# fact_invoice

## Purpose

Captures invoice generation and billing information.

Supports:

* Revenue Analytics
* Billing Analytics
* Collections Analytics
* Invoice Aging
* Forecasting Inputs

## Grain

One row per invoice.

## Primary Key


invoice_id


## Foreign Keys


tenant_key

customer_key

subscription_key

product_key

pricing_plan_key


## Measures


gross_amount

discount_amount

tax_amount

net_amount


## Attributes


invoice_number

invoice_status

currency

invoice_date

due_date

paid_date


## Audit


created_timestamp
updated_timestamp


---

# fact_payment

## Purpose

Captures payment attempts and outcomes.

Supports:

* Collections Analytics
* Payment Success Rate
* Failed Payment Analysis
* Revenue Realization
* Cash Flow Analytics

## Grain

One row per payment attempt.

A single invoice may have multiple payment attempts.

## Primary Key


payment_id


## Foreign Keys


tenant_key

customer_key

subscription_key

product_key

pricing_plan_key


## Degenerate Dimension


invoice_id


Invoice remains a business reference attribute and does not require a separate dimension.

## Measures


payment_amount


## Attributes


payment_status

payment_method

payment_gateway

gateway_transaction_id

failure_reason

payment_attempt_timestamp

payment_processed_timestamp


## Audit


created_timestamp
updated_timestamp


---

# fact_usage_event

## Purpose

Captures user activity within the application.

Supports:

* DAU
* MAU
* Stickiness
* Feature Adoption
* Customer Health
* Product Analytics
* AI Feature Engineering

## Grain

One row per user activity event.

## Primary Key


usage_event_id


## Foreign Keys


tenant_key

customer_key

user_key

product_key

feature_key


## Measures


event_count


Default value:


1


Optional:


event_value


for duration, consumption, or usage-based metrics.

## Attributes


event_type

event_timestamp

session_id

device_type

platform


## Audit


created_timestamp


---

# Fact-Dimension Matrix

| Fact                    | Tenant | Customer | Subscription | Product | Pricing Plan | User | Feature |
| ----------------------- | ------ | -------- | ------------ | ------- | ------------ | ---- | ------- |
| fact_subscription_event | Y      | Y        | Y            | Y       | Y            | N    | N       |
| fact_invoice            | Y      | Y        | Y            | Y       | Y            | N    | N       |
| fact_payment            | Y      | Y        | Y            | Y       | Y            | N    | N       |
| fact_usage_event        | Y      | Y        | N            | Y       | N            | Y    | Y       |

---

# Star Schema Relationships

## Revenue Domain

fact_subscription_event


fact_subscription_event
    ├── dim_tenant
    ├── dim_customer
    ├── dim_subscription
    ├── dim_product
    └── dim_pricing_plan


fact_invoice


fact_invoice
    ├── dim_tenant
    ├── dim_customer
    ├── dim_subscription
    ├── dim_product
    └── dim_pricing_plan


fact_payment


fact_payment
    ├── dim_tenant
    ├── dim_customer
    ├── dim_subscription
    ├── dim_product
    └── dim_pricing_plan


## Product Adoption Domain

fact_usage_event


fact_usage_event
    ├── dim_tenant
    ├── dim_customer
    ├── dim_user
    ├── dim_product
    └── dim_feature


---

# Partitioning Strategy

## fact_usage_event

Partition By:


event_timestamp


Cluster By:


customer_key
user_key
feature_key


## fact_payment

Partition By:


payment_processed_timestamp


Cluster By:


customer_key
subscription_key


## fact_invoice

Partition By:


invoice_date


Cluster By:


customer_key
subscription_key


## fact_subscription_event

Partition By:


event_timestamp


Cluster By:


customer_key
subscription_key


---

# Late Arriving Data Strategy

All fact tables shall support late-arriving data.

Approach:

1. Lookup dimensions using business key and event date.
2. If lookup fails, assign UNKNOWN surrogate key (-1).
3. Reprocess during reconciliation and backfill runs.

---

# Backfill Strategy

Historical data shall be loaded using business event dates rather than ingestion dates.

Dimension lookups shall use:


Business Key
+
Event Date


to retrieve the correct SCD2 version of the dimension.

This ensures historical accuracy of facts during backfill operations.

---

# Date Dimension Decision

The MVP implementation shall not include a Date Dimension.

Rationale:

1. BigQuery provides rich native DATE and TIMESTAMP functionality.
2. No fiscal calendar requirements currently exist.
3. Simplifies the dimensional model.
4. Reduces ETL complexity.

Date dimensions may be introduced in future releases if fiscal calendars, holiday calendars, or custom reporting calendars become business requirements.

---

# Section Status

# Dimensional Model Status

Section 3: Dimensional Data Model

Status: APPROVED AND FROZEN

Version: 1.0



---
# Section 4: Data Layer Architecture (Bronze, Silver, Gold)

## Purpose

This section defines the data flow architecture of the InsightFlow platform and establishes the responsibilities of each data layer.

The architecture follows a modern lakehouse approach consisting of:


Source Systems
    ↓
Landing
    ↓
Bronze
    ↓
Silver
    ↓
Gold


The objective is to separate:

* Raw data ingestion
* Business data processing
* Business intelligence and AI outputs

---

# 4.1 Data Layer Principles

## Landing Layer

### Purpose

Temporary ingestion zone for incoming data.

### Characteristics

* Raw files
* Raw API payloads
* Raw event streams
* Short retention period
* No transformations

---

## Bronze Layer

### Purpose

Persistent raw copy of source data.

### Characteristics

* Append-only
* Schema preserved from source
* Minimal transformations
* Full auditability
* Historical replay support

---

## Silver Layer

### Purpose

Trusted business layer and system of record for analytics.

### Characteristics

* Deduplicated
* Validated
* Standardized
* Business rules applied
* SCD processing performed
* Conformed dimensions
* Business facts

Silver serves as the Single Source of Truth for:

* Reporting
* Analytics
* Data Science
* Forecasting
* AI Applications
* GenAI Applications

---

## Gold Layer

### Purpose

Business consumption layer.

### Characteristics

* KPI tables
* Aggregate tables
* AI feature tables
* Forecast outputs
* Recommendation outputs

Gold contains business insights rather than raw business transactions.

---

# 4.2 Source System Inventory

## Master Data Management (MDM)

### Owned Entities


Product
Pricing Plan
Country
Region
Customer Segment
Acquisition Channel


---

## CRM Domain

### Owned Entities


Customer


---

## Subscription Domain

### Owned Entities


Subscription


---

## Billing Domain

### Owned Entities


Invoice
Paymentf


---

## Application Domain

### Owned Entities


User
Feature
Usage Event


---

# 4.3 Bronze Layer Objects

## Master Data Domain


bronze_product

bronze_pricing_plan

bronze_country

bronze_region

bronze_customer_segment

bronze_acquisition_channel


---

## CRM Domain


bronze_customer


---

## Subscription Domain


bronze_subscription

bronze_subscription_event


---

## Billing Domain


bronze_invoice

bronze_payment


---

## Application Domain


bronze_user

bronze_feature

bronze_usage_event


---

# 4.4 Silver Layer Objects

The Silver Layer contains the trusted business model for the organization.

---

## Dimensions


dim_tenant

dim_customer

dim_subscription

dim_product

dim_pricing_plan

dim_feature

dim_user

dim_country

dim_region

dim_customer_segment

dim_acquisition_channel


---

## Facts


fact_subscription_event

fact_invoice

fact_payment

fact_usage_event


---

# 4.5 Silver Layer Processing Rules

## Customer Processing

Transformations:

* Deduplication
* Data validation
* Country enrichment
* Region enrichment
* SCD2 processing

Output:


dim_customer


---

## Subscription Processing

Transformations:

* Deduplication
* Status standardization
* Subscription validation
* SCD2 processing

Output:


dim_subscription


---

## Product Processing

Transformations:

* Product standardization
* Category validation
* Metadata validation

Output:


dim_product


---

## Pricing Plan Processing

Transformations:

* Pricing validation
* Billing frequency standardization
* Seat limit validation
* SCD2 processing

Output:


dim_pricing_plan


---

## User Processing

Transformations:

* Identity validation
* Customer mapping
* Status standardization
* SCD2 processing

Output:


dim_user


---

## Invoice Processing

Transformations:

* Invoice validation
* Amount validation
* Currency standardization

Output:


fact_invoice


---

## Payment Processing

Transformations:

* Payment validation
* Gateway normalization
* Payment status standardization

Output:


fact_payment


---

## Usage Event Processing

Transformations:

* Event validation
* Deduplication
* Session enrichment
* User enrichment
* Feature enrichment

Output:


fact_usage_event


---

# 4.6 Subscription Event Processing

Subscription events may originate from two sources:

## Source Generated Events

Examples:


SUBSCRIPTION_CREATED

SUBSCRIPTION_RENEWED

SUBSCRIPTION_CANCELLED

PLAN_UPGRADED


---

## Warehouse Derived Events

Events generated by comparing historical subscription versions.

Example:


Version 1
100 Seats

Version 2
150 Seats


Derived Event:


SEATS_INCREASED

event_seat_delta = 50


---

## Processing Flow


Source Events
        +
Derived Events
        ↓
silver_subscription_event
        ↓
fact_subscription_event


---

# 4.7 Gold Layer Objects

Gold contains business-consumption artifacts.

---

## KPI Tables

Examples:


agg_daily_arr

agg_monthly_mrr

agg_customer_retention

agg_customer_adoption


---

## Revenue Aggregates

Examples:


agg_daily_revenue

agg_monthly_revenue

agg_subscription_growth


---

## AI Feature Tables

Examples:


feature_customer_health

feature_churn_prediction

feature_expansion_opportunity


---

## Forecast Outputs

Examples:


forecast_revenue

forecast_arr

forecast_customer_growth


---

## Recommendation Outputs

Examples:


customer_recommendation

next_best_action


---

# 4.8 Architectural Principles

1. Bronze stores raw source data.
2. Silver stores trusted business data.
3. Gold stores business insights and AI outputs.
4. Silver is the Single Source of Truth.
5. All reporting, AI, and forecasting workloads consume Silver or Gold.
6. Subscription events support both source-generated and warehouse-derived event creation.
7. Master Data and Transactional Data are managed separately.
8. Gold contains no raw operational transactions.

---

# Section Status

Section 4: Data Layer Architecture

Status: APPROVED AND FROZEN

Version: 1.0
-----

# Section 5: Physical Data Model

## Purpose

This section defines the physical implementation standards for InsightFlow, including dataset organization, naming conventions, datatype standards, key management, SCD strategy, storage architecture, partitioning, clustering, incremental processing, and metadata management.

---

# 5.1 Physical Architecture Principles

## Principle 1: Business-Driven Design

The physical model shall implement the approved:

* Conceptual Model
* Logical Model
* Dimensional Model

Technology decisions must support business requirements.

---

## Principle 2: Single Source of Truth

The Silver layer shall serve as the canonical business layer.

All dimensions and facts shall be maintained in Silver.

---

## Principle 3: Gold for Consumption

Gold shall contain:

* KPI Tables
* Aggregate Tables
* Forecast Outputs
* AI Feature Tables
* Executive Scorecards

Gold shall not contain raw transactional data.

---

## Principle 4: Auditability

All data entering the platform shall be traceable back to its original source.

Raw source data shall be archived in GCS.

---

## Principle 5: Cloud-Native Design

The platform shall be optimized for:

* Kafka
* GCS
* BigQuery
* Airflow (Cloud Composer)
* Dataproc (optional)

---

# 5.2 Physical Storage Architecture

## Data Flow


Source Systems
      ↓
Kafka
      ↓
GCS Landing (Raw Archive)
      ↓
BigQuery Bronze
      ↓
BigQuery Silver
      ↓
BigQuery Gold


---

## Landing Layer

Technology:


Google Cloud Storage (GCS)


Purpose:

* Raw data archive
* Replay capability
* Audit support
* Backfill support

Examples:


gs://insightflow/customer/
gs://insightflow/subscription/
gs://insightflow/payment/


---

## Bronze Layer

Technology:


BigQuery Dataset


Purpose:

* Raw business records
* Minimal transformation
* Historical persistence

Examples:


bronze.customer
bronze.subscription
bronze.invoice
bronze.payment
bronze.usage_event


---

## Silver Layer

Technology:


BigQuery Dataset


Purpose:

* Canonical business layer
* Dimensions
* Facts
* SCD implementation

Examples:


silver.dim_customer
silver.dim_subscription
silver.dim_product
silver.dim_pricing_plan

silver.fact_subscription_event
silver.fact_invoice
silver.fact_payment
silver.fact_usage_event


---

## Gold Layer

Technology:


BigQuery Dataset


Purpose:

* KPIs
* Aggregates
* Forecasting
* AI outputs

Examples:


gold.agg_daily_arr
gold.customer_health_score
gold.forecast_revenue


---

## Metadata Layer

Technology:


BigQuery Dataset


Purpose:

* Audit
* Monitoring
* Data Quality
* Watermark Management

Examples:


metadata.pipeline_run
metadata.pipeline_watermark
metadata.data_quality_results
metadata.reconciliation_summary


---

# 5.3 Naming Standards

## Dataset Naming


landing
bronze
silver
gold
metadata


---

## Dimension Naming

Pattern:


dim_<entity>


Examples:


dim_customer
dim_subscription
dim_product
dim_pricing_plan


---

## Fact Naming

Pattern:


fact_<business_event>


Examples:


fact_subscription_event
fact_invoice
fact_payment
fact_usage_event


---

## Aggregate Naming

Pattern:


agg_<metric>


Examples:


agg_daily_arr
agg_monthly_revenue


---

## Forecast Naming

Pattern:


forecast_<metric>


Examples:


forecast_revenue
forecast_arr


---

## Feature Naming

Pattern:


feature_<business_feature>


Examples:


feature_customer_health
feature_churn_prediction


---

## Column Naming

All columns shall follow:


snake_case


Examples:


customer_id
subscription_id
invoice_amount
event_timestamp


---

# 5.4 Data Type Standards

| Category       | Datatype  |
| -------------- | --------- |
| Business Keys  | STRING    |
| Surrogate Keys | INT64     |
| Currency       | NUMERIC   |
| Counts         | INT64     |
| Date           | DATE      |
| Timestamp      | TIMESTAMP |
| Boolean        | BOOLEAN   |
| Status         | STRING    |
| JSON Payload   | JSON      |

---

## Timestamp Standard

All timestamps shall be:


UTC
ISO-8601


Example:


2026-06-12T14:30:25Z


---

# 5.5 Surrogate Key Strategy

## Standard

Business Key:


STRING


Surrogate Key:


INT64


---

## Fact Tables

Fact tables shall retain:


Business Key
+
Surrogate Key


Examples:


customer_key
customer_id

subscription_key
subscription_id


Purpose:

* Lineage
* Debugging
* Reconciliation
* Historical tracking

---

## Unknown Member

Reserved Key:


-1


Purpose:

* Missing dimensions
* Late arriving dimensions
* Reconciliation support

---

# 5.6 Slowly Changing Dimension Strategy

## SCD2 Dimensions


dim_customer

dim_subscription

dim_pricing_plan

dim_user


---

## SCD1 Dimensions


dim_product

dim_feature

dim_country

dim_region

dim_customer_segment

dim_acquisition_channel


---

## Standard SCD2 Columns


effective_from_date

effective_to_date

is_current


---

## Open End Date

Current records:


effective_to_date = '9999-12-31'


---

## Fact Resolution

Facts shall resolve dimensions using:


business_key
+
event_date


to identify the correct SCD version.

---

# 5.7 Partitioning Standards

## fact_usage_event

Partition:


event_timestamp


Granularity:


DAY


---

## fact_subscription_event

Partition:


event_timestamp


Granularity:


DAY


---

## fact_payment

Partition:


payment_processed_timestamp


Granularity:


DAY


---

## fact_invoice

Partition:


invoice_date


Granularity:


MONTH


---

## Dimensions

No partitioning initially.

---

# 5.8 Clustering Standards

## fact_usage_event

Cluster By:


customer_key
user_key
feature_key


---

## fact_subscription_event

Cluster By:


customer_key
subscription_key


---

## fact_payment

Cluster By:


customer_key
subscription_key


---

## fact_invoice

Cluster By:


customer_key
subscription_key


---

# 5.9 Incremental Processing Strategy

## Tier 1

Preferred:


CDC


Examples:


Customer

Subscription


---

## Tier 2

Timestamp-Based Incremental

Pattern:

sql
WHERE updated_timestamp > watermark


---

## Tier 3

Snapshot Comparison

Used when CDC and timestamps are unavailable.

---

## Watermark Management

Control Table:


metadata.pipeline_watermark


Attributes:


pipeline_name
last_successful_timestamp


---

## Reprocessing Support

All pipelines shall support:


start_date
end_date


for backfills and reprocessing.

---

# 5.10 Metadata & Audit Framework

## Pipeline Execution

Table:


metadata.pipeline_run


Attributes:


run_id
pipeline_name
start_timestamp
end_timestamp
status
records_processed
records_failed
error_message


---

## Watermark Tracking

Table:


metadata.pipeline_watermark


---

## Data Quality Monitoring

Table:


metadata.data_quality_results


---

## Reconciliation Tracking

Table:


metadata.reconciliation_summary


---

## Standard Audit Columns

### Dimensions


created_timestamp

updated_timestamp

source_system


---

### Facts


event_timestamp

created_timestamp

source_system


---

## Error Handling

Missing dimensions shall not fail pipelines.

Fallback:


surrogate_key = -1


Issue shall be logged and reconciled later.

---

# Section Status

Section 5: Physical Data Model

Status: APPROVED AND FROZEN

Version: 1.0



----

# Section 6: Data Quality Framework

## Purpose

This section defines the Data Quality (DQ) standards, validation framework, monitoring processes, alerting mechanisms, and remediation strategy for InsightFlow.

The objective is to ensure reliable, trustworthy, and business-consumable data while minimizing operational disruptions.

---

# 6.1 Data Quality Principles

## Principle 1: Data Availability Over Perfection

The platform shall prioritize data availability whenever possible.

Preferred:


95% accurate dashboard with alerts


over


No dashboard because a few records failed validation


---

## Principle 2: Tiered Error Handling

Errors shall be classified into severity levels.

### Critical Errors

Pipeline execution stops.

Examples:


Source unavailable

Schema corruption

Unreadable files

Missing mandatory source tables

Infrastructure failures


---

### Non-Critical Errors

Pipeline continues.

Examples:


Missing dimension records

Invalid optional fields

Unknown country codes

Late arriving dimensions

Minor data inconsistencies


Records are loaded using approved fallback rules.

---

## Principle 3: Shift Left Validation

Data quality checks shall be performed as early as possible.


Landing
    ↓
Bronze Validation
    ↓
Silver Validation
    ↓
Gold Validation


---

## Principle 4: Every DQ Failure Must Be Visible

No data quality issue shall fail silently.

Every violation must:


Be Logged

Be Monitored

Be Alerted

Be Traceable


---

# 6.2 Data Quality Dimensions

The platform shall monitor six core DQ dimensions.

---

## Completeness

Validates presence of required fields.

Examples:


customer_id NOT NULL

subscription_id NOT NULL

invoice_amount NOT NULL


---

## Uniqueness

Validates duplicate records.

Examples:


customer_id unique

subscription_id unique

invoice_id unique


---

## Validity

Validates datatype and format.

Examples:


Date format

Timestamp format

Currency datatype

Enum values


---

## Consistency

Validates business consistency.

Examples:


Subscription customer must exist

Invoice subscription must exist

Payment invoice must exist


---

## Timeliness

Validates freshness.

Examples:


Customer updates received within SLA

Usage events arriving within SLA


---

## Referential Integrity

Validates entity relationships.

Examples:


Customer exists

Product exists

Pricing Plan exists


---

# 6.3 Standard Validation Rules

## Customer

Checks:


customer_id NOT NULL

customer_id UNIQUE

customer_status IN Approved Values

created_timestamp VALID UTC


---

## Subscription

Checks:


subscription_id NOT NULL

customer_id EXISTS

plan_id EXISTS

start_date <= end_date


---

## Invoice

Checks:


invoice_id NOT NULL

invoice_amount >= 0

subscription_id EXISTS


---

## Payment

Checks:


payment_id NOT NULL

payment_amount >= 0

invoice_id EXISTS


---

## Usage Events

Checks:


event_id NOT NULL

event_timestamp VALID

customer_id EXISTS

feature_id EXISTS


---

# 6.4 Data Quality Severity Framework

## Severity 1 (Critical)

Action:


Pipeline Fails
Immediate Alert


Examples:


Source Missing

Schema Corruption

File Corruption

Critical Datatype Failure


---

## Severity 2 (High)

Action:


Pipeline Continues

Alert Generated

Manual Review Required


Examples:


> 5% Missing Customer Keys

Large Duplicate Spike

Reference Data Missing


---

## Severity 3 (Medium)

Action:


Pipeline Continues

Issue Logged

Daily Review


Examples:


Unknown Dimensions

Small Duplicate Counts

Minor Data Delays


---

## Severity 4 (Low)

Action:


Logged Only


Examples:


Optional Field Missing

Minor Formatting Issues


---

# 6.5 Unknown Member Strategy

Approved Unknown Key:


-1


Used For:


Late Arriving Dimensions

Missing Reference Data

Data Quality Exceptions


---

## Example

Customer Missing:


customer_key = -1


Fact record still loads.

---

## Reconciliation

Scheduled jobs shall attempt correction when missing dimensions become available.

---

# 6.6 Data Quality Scorecard

Every table shall have a DQ score.

Formula:


DQ Score =
(Passed Checks / Total Checks)
× 100


---

## Thresholds

| Score   | Status   |
| ------- | -------- |
| >= 95%  | Healthy  |
| 90%-95% | Warning  |
| < 90%   | Critical |

---

# 6.7 Metadata & Audit Integration

Data quality results shall be stored in:


metadata.data_quality_results


---

Mandatory Attributes:


run_id

table_name

check_name

check_status

failed_record_count

execution_timestamp

severity


---

# 6.8 Alerting Framework

## Purpose

Automatically notify stakeholders when data quality issues or pipeline failures occur.

---

## Alert Channels

Primary:


Microsoft Teams

Email


Optional:


Slack

PagerDuty

ServiceNow


---

## Alert Categories

### Pipeline Failure Alert

Triggered When:


Pipeline Status = FAILED


Recipients:


Data Engineering Team


Alert Example:


Pipeline: subscription_load

Status: FAILED

Time: 2026-06-13 09:30 UTC

Error:
Source Table Not Reachable


---

### High Severity DQ Alert

Triggered When:


DQ Score < 90%

OR

Critical Validation Failure


Recipients:


Data Engineering

Business Owner


Alert Example:


Table: dim_customer

Issue:
12% Missing customer_id

Severity: HIGH


---

### Freshness Alert

Triggered When:


SLA Breach


Examples:


Usage Events Delayed > 15 Minutes

Customer Feed Delayed > 1 Hour

Invoice Feed Delayed > 24 Hours


---

### Unknown Dimension Alert

Triggered When:


Unknown Key %
exceeds threshold


Examples:


customer_key = -1

product_key = -1

plan_key = -1


Threshold:


> 1%


---

# 6.9 Data Quality Dashboards

The platform shall provide operational dashboards displaying:


Pipeline Success Rate

DQ Scores

Failed Checks

Unknown Dimension %

Data Freshness

SLA Compliance

Error Trends


---

# 6.10 Remediation Framework

## Automatic Remediation

Examples:


Retry Failed Pipelines

Reprocess Late Files

Dimension Reconciliation Jobs


---

## Manual Remediation

Examples:


Fix Source Data

Backfill Missing Data

Correct Reference Data


---

## Ownership

Every DQ issue shall have:


Assigned Owner

Created Timestamp

Resolution Timestamp

Current Status


---

# Section Status

Section 6: Data Quality Framework

Status: APPROVED AND FROZEN

Version: 1.0
---
# Section 7: Security & Governance

## Purpose

This section defines the security, access control, governance, auditability, and compliance framework for InsightFlow.

The objective is to ensure that data remains secure, compliant, discoverable, and accessible only to authorized users while maintaining operational efficiency.

---

# 7.1 Security Principles

## Principle 1: Least Privilege Access

Users shall be granted only the minimum access required to perform their responsibilities.

---

## Principle 2: Role-Based Access Control (RBAC)

Access shall be assigned through roles rather than individual permissions.

Benefits:


Simplified Administration

Consistent Security

Scalable Governance


---

## Principle 3: Data Ownership

Every entity, dataset, and KPI shall have a designated business owner.

---

## Principle 4: Auditability

All access, modifications, and operational activities shall be auditable.

---

## Principle 5: Separation of Environments

Development, testing, and production environments shall remain logically isolated.

---

# 7.2 Environment Strategy

## Environments


DEV

UAT

PROD


---

## DEV

Purpose:


Development

Unit Testing

Feature Validation


Characteristics:


Synthetic Data Preferred

Limited Access Controls

Frequent Changes


---

## UAT

Purpose:


Business Testing

Integration Testing

Release Validation


Characteristics:


Production-like Environment

Controlled Access

Pre-Production Validation


---

## PROD

Purpose:


Business Reporting

Operational Analytics

Executive Dashboards

AI Applications


Characteristics:


Strict Access Controls

Full Auditability

High Availability


---

# 7.3 Role-Based Access Control (RBAC)

## Data Engineer

Permissions:


Read/Write Bronze

Read/Write Silver

Read Metadata

Manage Pipelines


---

## Analytics Engineer

Permissions:


Read Silver

Read/Write Gold

Read Metadata


---

## Business Analyst

Permissions:


Read Gold

Read Approved KPI Tables


---

## Product Team

Permissions:


Read Product KPIs

Read Usage Metrics

Read Customer Health Metrics


---

## Executive User

Permissions:


Read Executive Dashboards

Read Scorecards

Read Approved KPI Views


---

## Platform Administrator

Permissions:


Full Platform Access


---

# 7.4 Dataset Security Model

## Bronze Layer

Access:


Data Engineering Only


Reason:


Contains Raw Operational Data


---

## Silver Layer

Access:


Data Engineering

Analytics Engineering


Reason:


Canonical Business Layer


---

## Gold Layer

Access:


Business Users

Product Teams

Executives

Analytics Teams


Reason:


Business Consumption Layer


---

## Metadata Layer

Access:


Platform Team

Data Engineering


---

# 7.5 Service Account Strategy

## Principle

Applications shall not use personal user accounts.

---

## Service Accounts

Examples:


sa-airflow

sa-kafka-consumer

sa-data-quality

sa-forecasting


---

## Benefits


Traceability

Automation

Credential Isolation


---

# 7.6 Data Encryption

## Data In Transit

Encryption:


TLS


Applicable To:


Kafka

Airflow

BigQuery

APIs

GCS


---

## Data At Rest

Encryption:


Google Managed Encryption Keys


Supported Future Option:


Customer Managed Encryption Keys (CMEK)


---

# 7.7 Sensitive Data Management

## Sensitive Data Examples


Email Address

Phone Number

Physical Address

Payment Information


---

## Principle

Sensitive data shall only be exposed to authorized users.

---

## Masking Strategy

Examples:


john.doe@email.com

↓

j***@email.com



9876543210

↓

98******10


---

## Access Control

Sensitive attributes shall be protected using:


Column-Level Security


where required.

---

# 7.8 Audit Logging

## Objective

Provide traceability across the platform.

---

## Audit Categories

### Data Access

Tracks:


Who Accessed Data

When

What Dataset


---

### Pipeline Activity

Tracks:


Pipeline Execution

Failures

Retries

Backfills


---

### Administrative Activity

Tracks:


Role Changes

Permission Changes

Configuration Updates


---

## Audit Retention

Minimum Retention:


1 Year


---

# 7.9 Data Lineage

## Objective

Track movement of data from source to consumption.

---

## Lineage Scope


Source System

Kafka Topic

GCS Landing

Bronze Table

Silver Table

Gold Table

Dashboard / KPI


---

## Benefits


Impact Analysis

Root Cause Analysis

Regulatory Compliance


---

# 7.10 Governance Framework

## Data Ownership

Every entity shall have:


Business Owner

Technical Owner


---

## KPI Ownership

Every KPI shall have:


Business Owner

Approved Definition

Approved Formula


---

## Change Management

Changes requiring approval:


Business Key Changes

Schema Changes

KPI Formula Changes

Source System Changes


---

# 7.11 Compliance & Retention

## Data Retention

### GCS Raw Archive

Retention:


7 Years


---

### Bronze

Retention:


7 Years


---

### Silver

Retention:


Indefinite


---

### Gold

Retention:


Rebuildable


---

### Metadata

Retention:


3 Years


---

# 7.12 Security Monitoring

Security events shall be monitored for:


Unauthorized Access Attempts

Permission Violations

Failed Authentication

Excessive Data Access

Suspicious Activity


---

## Alerting

Security alerts shall be routed through:


Email

Microsoft Teams


using the centralized alerting framework.

---

# Section Status

Section 7: Security & Governance

Status: APPROVED AND FROZEN

Version: 1.0


---

# Section 9: Orchestration & Pipeline Design

## Purpose

This section defines the orchestration framework, pipeline architecture, ingestion patterns, processing standards, monitoring framework, retry mechanisms, and backfill strategy for InsightFlow.

The objective is to ensure reliable, scalable, observable, and recoverable data pipelines across the platform.

---

# 9.1 Pipeline Design Principles

## Principle 1: Metadata-Driven Processing

Pipeline execution shall be controlled through metadata tables wherever possible.

Examples:


metadata.pipeline_run

metadata.pipeline_watermark

metadata.data_quality_results

metadata.alert_log


---

## Principle 2: Idempotent Processing

Pipelines must support multiple executions without generating duplicate records.

Examples:


MERGE Operations

CDC Processing

Watermark-Based Loads


---

## Principle 3: Restartable Pipelines

Pipeline failures shall allow restart from the last successful checkpoint.

---

## Principle 4: Observable Pipelines

Every pipeline execution shall generate operational metadata for:


Execution Tracking

Monitoring

Alerting

Audit


---

## Principle 5: Reusable Framework

Pipeline logic shall be reusable across entities and business domains.

---

# 9.2 Ingestion Architecture

## Streaming Ingestion

Primary ingestion mechanism:


Kafka


Architecture:


Source Systems
      ↓
Kafka
      ↓
GCS Landing (Raw Archive)
      ↓
BigQuery Bronze


---

## Batch Ingestion

Supported for:


Files

APIs

External Partner Data

Reference Data


Architecture:


Source
      ↓
GCS Landing
      ↓
BigQuery Bronze


---

## Landing Layer

Technology:


Google Cloud Storage (GCS)


Purpose:


Raw Data Archive

Replay Support

Audit Support

Backfill Support


---

# 9.3 Airflow Orchestration Architecture

## Orchestration Platform

Technology:


Apache Airflow

(Google Cloud Composer)


---

## DAG Design Strategy

Approved Model:


Hybrid / Entity-Based DAG Architecture


---

## Pipeline DAGs


customer_pipeline_dag

subscription_pipeline_dag

invoice_pipeline_dag

payment_pipeline_dag

usage_event_pipeline_dag

product_pipeline_dag

pricing_plan_pipeline_dag


---

## Consumption Layer DAGs


gold_kpi_dag

forecasting_dag

customer_health_dag


---

## DAG Structure

Each entity DAG shall follow:


Extract
    ↓
Landing Validation
    ↓
Bronze Load
    ↓
DQ Validation
    ↓
Silver Load
    ↓
Metadata Update
    ↓
Alert Generation


---

# 9.4 Bronze to Silver Processing

## Objective

Transform raw operational records into canonical business entities.

---

## Processing Method

Preferred:


CDC


Fallback:


Timestamp Incremental


---

## Transformations

Examples:


Data Cleansing

Datatype Standardization

Business Rule Validation

Surrogate Key Resolution

SCD Processing


---

## Output

Dimensions:


dim_customer

dim_subscription

dim_product

dim_pricing_plan


Facts:


fact_subscription_event

fact_invoice

fact_payment

fact_usage_event


---

# 9.5 Silver to Gold Processing

## Objective

Generate business-ready analytical outputs.

---

## Outputs


KPI Tables

Aggregates

Forecasts

Customer Health Scores

Executive Scorecards


---

## Example Gold Tables


gold.agg_daily_arr

gold.customer_health_score

gold.forecast_revenue

gold.executive_scorecard


---

## Refresh Strategy

KPIs:


Hourly


Forecasts:


Daily


Executive Scorecards:


Daily


---

# 9.6 Retry & Recovery Framework

## Task Retry

Default Retry Count:


3


---

## Retry Strategy


Exponential Backoff


---

## Pipeline Recovery

Supported Mechanisms:


Task Restart

DAG Restart

Partial Reprocessing

Full Reprocessing


---

## Idempotency Requirement

All pipelines must support safe reruns.

Examples:


MERGE Operations

CDC Replay

Date Range Reprocessing


---

# 9.7 Backfill Framework

## Objective

Support historical reprocessing without affecting active workloads.

---

## Standard Parameters

All pipelines shall support:


start_date

end_date


---

## Supported Scenarios


Historical Loads

Data Corrections

Source Reprocessing

Dimension Rebuilds

Fact Rebuilds


---

## Backfill Execution

Example:


subscription_pipeline_dag

start_date = 2026-01-01

end_date = 2026-01-31


---

## Backfill Audit

All backfills shall be logged in:


metadata.pipeline_run


---

# 9.8 Watermark Management

## Purpose

Track incremental processing state.

---

## Metadata Table


metadata.pipeline_watermark


---

## Standard Attributes


pipeline_name

entity_name

last_successful_timestamp

updated_timestamp


---

## Usage

Example:

sql
WHERE updated_timestamp >
last_successful_timestamp


---

# 9.9 Monitoring Framework

## Operational Metadata

Pipeline monitoring shall be driven through metadata tables.

---

## Pipeline Execution Monitoring

Table:


metadata.pipeline_run


Tracks:


Start Time

End Time

Status

Records Processed

Records Failed

Execution Duration


---

## Data Quality Monitoring

Table:


metadata.data_quality_results


Tracks:


DQ Scores

Failed Checks

Severity

Violation Counts


---

## Alert Monitoring

Table:


metadata.alert_log


Tracks:


Alert Type

Severity

Status

Resolution Timestamp


---

# 9.10 Alerting Framework

## Alert Sources

Alerts may originate from:


Pipeline Failures

Data Quality Failures

Freshness Violations

SLA Breaches

Infrastructure Failures

Schema Validation Failures


---

## Alert Architecture


Airflow / Validation Framework
            ↓
      Alert Service
            ↓
Email
Microsoft Teams


---

## Alert Payload

Every alert shall include:


Alert ID

Timestamp

Severity

Pipeline Name

Entity Name

Environment

Run ID

Error Type

Error Description

Recommended Resolution


---

## Alert Audit

All alerts shall be stored in:


metadata.alert_log


---

## Future Integrations

The framework shall support future integration with:


Slack

PagerDuty

ServiceNow


without architectural changes.

---

# 9.11 Operational SLA Framework

## Streaming Pipelines

Target SLA:


< 5 Minutes


Examples:


Usage Events

Customer Events

Subscription Events


---

## Batch Pipelines

Target SLA:


< 24 Hours


Examples:


Invoices

Payments

Reference Data


---

## KPI Availability

Target SLA:


< 1 Hour


after source data availability.

---

# Section Status

Section 9: Orchestration & Pipeline Design

Status: APPROVED AND FROZEN

Version: 1.0




---
# Section 10: Semantic Layer & KPI Definitions

## Purpose

This section defines the business KPIs supported by InsightFlow, their ownership, calculation standards, and semantic governance principles. The objective is to establish a single, trusted definition for every business metric consumed by dashboards, reports, forecasting models, and AI applications.

---

# 10.1 Semantic Layer Principles

## Principle 1: Single Definition of Truth

Every KPI shall have one approved business definition and one approved calculation methodology.

---

## Principle 2: Silver is the Source Layer

All KPI calculations shall originate from:

* silver.fact_*
* silver.dim_*

Gold shall contain only KPI outputs, aggregates, forecasts, and AI-driven insights.

---

## Principle 3: Business Ownership

Every KPI shall have a designated business owner responsible for approving definition changes.

---

## Principle 4: Reusable Metrics

KPIs shall be defined once and reused across:

* Dashboards
* Reports
* Forecasting Models
* AI Agents
* Executive Scorecards

---

# 10.2 Revenue Intelligence KPIs

| KPI ID  | KPI Name                        | Business Owner |
| ------- | ------------------------------- | -------------- |
| KPI-001 | Monthly Recurring Revenue (MRR) | CFO            |
| KPI-002 | Annual Recurring Revenue (ARR)  | CFO            |
| KPI-003 | Revenue by Product              | CFO            |
| KPI-004 | Revenue by Product Category     | CFO, CEO       |
| KPI-005 | Revenue by Geography            | CFO            |
| KPI-006 | Revenue Growth %                | CFO, CEO       |

---

## KPI-001 Monthly Recurring Revenue (MRR)

Definition:

Monthly recurring revenue generated from active paid subscriptions.

Formula:

MRR = Sum(Subscription Monthly Value)

Where:

* Monthly Plan = Plan Price
* Quarterly Plan = Plan Price / 3
* Annual Plan = Plan Price / 12

Included:

* Active subscriptions
* Paid subscriptions
* Recurring seat charges

Excluded:

* Trial subscriptions
* Taxes
* One-time charges
* Refunds

Source Tables:

* dim_subscription
* dim_pricing_plan

---

## KPI-002 Annual Recurring Revenue (ARR)

Formula:

ARR = MRR × 12

Source Tables:

* KPI-001 MRR

---

## KPI-003 Revenue by Product

Formula:

Sum(MRR) grouped by Product

---

## KPI-004 Revenue by Product Category

Formula:

Sum(MRR) grouped by Product Category

---

## KPI-005 Revenue by Geography

Formula:

Sum(MRR) grouped by Country / Region

---

## KPI-006 Revenue Growth %

Formula:

(Current Period Revenue − Previous Period Revenue) / Previous Period Revenue × 100

---

# 10.3 Subscription Lifecycle Intelligence KPIs

| KPI ID  | KPI Name                   | Business Owner     |
| ------- | -------------------------- | ------------------ |
| KPI-007 | New Subscriptions          | Revenue Operations |
| KPI-008 | Renewed Subscriptions      | Revenue Operations |
| KPI-009 | Cancelled Subscriptions    | Revenue Operations |
| KPI-010 | Active Subscriptions       | Revenue Operations |
| KPI-011 | Grace Period Subscriptions | Revenue Operations |
| KPI-012 | Expired Subscriptions      | Revenue Operations |

---

## KPI-007 New Subscriptions

Formula:

Count(subscription_created events)

Source:

* fact_subscription_event

---

## KPI-008 Renewed Subscriptions

Formula:

Count(subscription_renewed events)

Source:

* fact_subscription_event

---

## KPI-009 Cancelled Subscriptions

Formula:

Count(subscription_cancelled events)

Source:

* fact_subscription_event

---

## KPI-010 Active Subscriptions

Formula:

Count(active subscriptions)

Condition:

subscription_status = 'ACTIVE'

Source:

* dim_subscription

---

## KPI-011 Grace Period Subscriptions

Formula:

Count(subscriptions in grace period)

---

## KPI-012 Expired Subscriptions

Formula:

Count(expired subscriptions)

---

# 10.4 Product Adoption Intelligence KPIs

| KPI ID  | KPI Name                   | Business Owner |
| ------- | -------------------------- | -------------- |
| KPI-013 | Daily Active Users (DAU)   | Product Team   |
| KPI-014 | Monthly Active Users (MAU) | Product Team   |
| KPI-015 | Feature Adoption Rate      | Product Team   |
| KPI-016 | Seat Utilization           | Product Team   |
| KPI-017 | Most Used Features         | Product Team   |

---

## KPI-013 Daily Active Users (DAU)

Formula:

Count(Distinct User) per Day

Source:

* fact_usage_event

---

## KPI-014 Monthly Active Users (MAU)

Formula:

Count(Distinct User) per Month

Source:

* fact_usage_event

---

## KPI-015 Feature Adoption Rate

Formula:

Users Using Feature / Eligible Users × 100

Source:

* fact_usage_event
* dim_feature

---

## KPI-016 Seat Utilization

Formula:

Active Users / Purchased Seats × 100

Source:

* fact_usage_event
* dim_subscription

---

## KPI-017 Most Used Features

Formula:

Rank Features by Usage Count

Source:

* fact_usage_event

---

# 10.5 Customer Health Intelligence KPIs

| KPI ID  | KPI Name              | Business Owner   |
| ------- | --------------------- | ---------------- |
| KPI-018 | Customer Health Score | Customer Success |
| KPI-019 | Healthy Customers     | Customer Success |
| KPI-020 | At-Risk Customers     | Customer Success |
| KPI-021 | Customer Tenure       | Customer Success |

---

## KPI-018 Customer Health Score

Formula:

* Product Usage = 40%
* Subscription Health = 20%
* Revenue Trend = 20%
* Support Signals = 20%

Score Range:

0-100

---

## KPI-019 Healthy Customers

Formula:

Customer Health Score ≥ 80

---

## KPI-020 At-Risk Customers

Formula:

Customer Health Score < 50

---

## KPI-021 Customer Tenure

Formula:

Current Date − Customer Acquisition Date

Source:

* dim_customer

---

# 10.6 Churn Intelligence KPIs

| KPI ID  | KPI Name            | Business Owner   |
| ------- | ------------------- | ---------------- |
| KPI-022 | Customer Churn Rate | Customer Success |
| KPI-023 | Gross Revenue Churn | CFO              |
| KPI-024 | Net Revenue Churn   | CFO              |
| KPI-025 | Churn by Product    | Product Team     |

---

## KPI-022 Customer Churn Rate

Formula:

Churned Customers / Opening Customers × 100

---

## KPI-023 Gross Revenue Churn

Formula:

Revenue Lost From Churned Customers / Beginning Revenue × 100

---

## KPI-024 Net Revenue Churn

Formula:

(Revenue Lost From Churned Customers − Expansion Revenue) / Beginning Revenue × 100

---

## KPI-025 Churn by Product

Formula:

Cancelled Subscriptions grouped by Product

---

# 10.7 Predictive Intelligence KPIs

| KPI ID  | KPI Name           | Business Owner   |
| ------- | ------------------ | ---------------- |
| KPI-026 | Forecasted Revenue | CFO              |
| KPI-027 | Forecasted Churn   | Customer Success |
| KPI-028 | At-Risk Revenue    | CFO              |

---

## KPI-026 Forecasted Revenue

Source:

* gold.forecast_revenue

---

## KPI-027 Forecasted Churn

Source:

* gold.forecast_churn

---

## KPI-028 At-Risk Revenue

Formula:

Revenue associated with At-Risk Customers

Source:

* Customer Health Model

---

# 10.8 Executive Intelligence KPIs

| KPI ID  | KPI Name                     | Business Owner |
| ------- | ---------------------------- | -------------- |
| KPI-029 | Executive Revenue Scorecard  | CEO            |
| KPI-030 | Executive Customer Scorecard | CEO            |
| KPI-031 | Product Penetration Rate     | CEO            |

---

## KPI-029 Executive Revenue Scorecard

Includes:

* ARR
* MRR
* Revenue Growth %
* Revenue by Product
* Revenue by Geography

---

## KPI-030 Executive Customer Scorecard

Includes:

* Active Customers
* Customer Churn Rate
* Healthy Customers
* At-Risk Customers

---

## KPI-031 Product Penetration Rate

Formula:

Customers Using Product / Eligible Customers × 100

---

# Section Status

Section 10: Semantic Layer & KPI Definitions

Status: APPROVED AND FROZEN

Version: 1.0


---

# Section 11: Data Contracts

## Purpose

This section defines the contractual agreement between source system owners and the InsightFlow Data Platform. Data contracts establish ownership, source-of-truth systems, refresh expectations, mandatory fields, data standards, and quality expectations to ensure consistent and reliable data ingestion.

---

# 11.1 Data Contract Principles

## Principle 1: Source Ownership

Every entity must have a clearly defined business owner responsible for data quality and schema changes.

---

## Principle 2: Source of Truth

Every entity shall have a single approved source system.

Example:


Customer          → CRM
Subscription      → Subscription Platform
Invoice           → Billing Platform
Payment           → Payment Gateway
Product           → MDM
Pricing Plan      → MDM


---

## Principle 3: Backward Compatibility

Schema changes must be communicated before implementation.

Examples:


New Columns            → Allowed

Column Removal         → Approval Required

Datatype Changes       → Approval Required

Business Key Changes   → Not Allowed


---

## Principle 4: Mandatory Business Keys

Business keys must:


Be Present

Be Unique

Be Stable

Never Be Reused


---

## Principle 5: Data Validation

All inbound data shall be validated against:


Datatype Rules

Nullability Rules

Allowed Values

Referential Integrity Rules


before publication into Silver.

---

# 11.2 Enterprise Data Standards

## Business Key Standard

Datatype:


STRING


Rules:


Not Null

Unique

Immutable


Examples:


customer_id

subscription_id

invoice_id

payment_id

product_id

plan_id


---

## Date Standard

Datatype:


DATE


Format:


YYYY-MM-DD


Example:


2026-06-12


Applicable Fields:


invoice_date

subscription_start_date

subscription_end_date


---

## Timestamp Standard

Datatype:


TIMESTAMP


Timezone:


UTC


Format:


ISO-8601


Example:


2026-06-12T14:30:25Z


Applicable Fields:


event_timestamp

created_timestamp

updated_timestamp

payment_processed_timestamp


---

## Currency Standard

Datatype:


NUMERIC


Rules:


No FLOAT Usage

Precision Preserved


Applicable Fields:


invoice_amount

payment_amount

subscription_amount

arr

mrr


---

## Boolean Standard

Allowed Values:


TRUE

FALSE


Not Allowed:


Y/N

1/0

Yes/No


---

## Status Standard

Status fields must contain approved enumerated values.

Example:


subscription_status

ACTIVE
CANCELLED
EXPIRED
GRACE_PERIOD


---

# 11.3 Customer Data Contract

| Attribute       | Value           |
| --------------- | --------------- |
| Entity          | Customer        |
| Business Owner  | CRM Team        |
| Source of Truth | CRM Platform    |
| Business Key    | customer_id     |
| Refresh Pattern | CDC / Streaming |
| SLA             | < 15 Minutes    |

## Mandatory Fields

| Field             | Type      | Nullable | Rule            |
| ----------------- | --------- | -------- | --------------- |
| customer_id       | STRING    | No       | Unique          |
| customer_name     | STRING    | No       | Not Blank       |
| customer_status   | STRING    | No       | Approved Values |
| created_timestamp | TIMESTAMP | No       | UTC             |
| updated_timestamp | TIMESTAMP | No       | UTC             |

---

# 11.4 Subscription Data Contract

| Attribute       | Value                 |
| --------------- | --------------------- |
| Entity          | Subscription          |
| Business Owner  | Revenue Operations    |
| Source of Truth | Subscription Platform |
| Business Key    | subscription_id       |
| Refresh Pattern | CDC / Streaming       |
| SLA             | < 15 Minutes          |

## Mandatory Fields

| Field               | Type   | Nullable | Rule               |
| ------------------- | ------ | -------- | ------------------ |
| subscription_id     | STRING | No       | Unique             |
| customer_id         | STRING | No       | Valid Customer     |
| plan_id             | STRING | No       | Valid Pricing Plan |
| subscription_status | STRING | No       | Approved Values    |
| start_date          | DATE   | No       | YYYY-MM-DD         |
| end_date            | DATE   | Yes      | YYYY-MM-DD         |

---

# 11.5 Invoice Data Contract

| Attribute       | Value            |
| --------------- | ---------------- |
| Entity          | Invoice          |
| Business Owner  | Finance          |
| Source of Truth | Billing Platform |
| Business Key    | invoice_id       |
| Refresh Pattern | Daily Batch      |
| SLA             | 24 Hours         |

## Mandatory Fields

| Field           | Type    | Nullable | Rule               |
| --------------- | ------- | -------- | ------------------ |
| invoice_id      | STRING  | No       | Unique             |
| subscription_id | STRING  | No       | Valid Subscription |
| invoice_date    | DATE    | No       | YYYY-MM-DD         |
| invoice_amount  | NUMERIC | No       | >= 0               |
| invoice_status  | STRING  | No       | Approved Values    |

---

# 11.6 Payment Data Contract

| Attribute       | Value           |
| --------------- | --------------- |
| Entity          | Payment         |
| Business Owner  | Finance         |
| Source of Truth | Payment Gateway |
| Business Key    | payment_id      |
| Refresh Pattern | Daily Batch     |
| SLA             | 24 Hours        |

## Mandatory Fields

| Field                       | Type      | Nullable | Rule            |
| --------------------------- | --------- | -------- | --------------- |
| payment_id                  | STRING    | No       | Unique          |
| invoice_id                  | STRING    | No       | Valid Invoice   |
| payment_amount              | NUMERIC   | No       | >= 0            |
| payment_status              | STRING    | No       | Approved Values |
| payment_processed_timestamp | TIMESTAMP | No       | UTC             |

---

# 11.7 Usage Event Data Contract

| Attribute       | Value                |
| --------------- | -------------------- |
| Entity          | Usage Event          |
| Business Owner  | Product Team         |
| Source of Truth | Application Platform |
| Business Key    | event_id             |
| Refresh Pattern | Streaming            |
| SLA             | < 5 Minutes          |

## Mandatory Fields

| Field           | Type      | Nullable | Rule           |
| --------------- | --------- | -------- | -------------- |
| event_id        | STRING    | No       | Unique         |
| user_id         | STRING    | No       | Valid User     |
| customer_id     | STRING    | No       | Valid Customer |
| feature_id      | STRING    | No       | Valid Feature  |
| event_timestamp | TIMESTAMP | No       | UTC            |

---

# 11.8 Product Data Contract

| Attribute       | Value        |
| --------------- | ------------ |
| Entity          | Product      |
| Business Owner  | Product Team |
| Source of Truth | MDM          |
| Business Key    | product_id   |
| Refresh Pattern | Daily Batch  |
| SLA             | 24 Hours     |

## Mandatory Fields

| Field            | Type   | Nullable | Rule            |
| ---------------- | ------ | -------- | --------------- |
| product_id       | STRING | No       | Unique          |
| product_name     | STRING | No       | Not Blank       |
| product_category | STRING | No       | Approved Values |

---

# 11.9 Pricing Plan Data Contract

| Attribute       | Value              |
| --------------- | ------------------ |
| Entity          | Pricing Plan       |
| Business Owner  | Revenue Operations |
| Source of Truth | MDM                |
| Business Key    | plan_id            |
| Refresh Pattern | Daily Batch        |
| SLA             | 24 Hours           |

## Mandatory Fields

| Field             | Type    | Nullable | Rule            |
| ----------------- | ------- | -------- | --------------- |
| plan_id           | STRING  | No       | Unique          |
| plan_name         | STRING  | No       | Not Blank       |
| billing_frequency | STRING  | No       | Approved Values |
| base_price        | NUMERIC | No       | >= 0            |

---

# 11.10 Contract Enforcement Framework

## Validation Layer

All inbound data shall be validated in Bronze/Silver ingestion pipelines.

Validation Categories:


Schema Validation

Datatype Validation

Mandatory Field Validation

Referential Integrity Validation

Business Rule Validation


---

## Contract Violations

Contract violations shall not stop ingestion into Bronze.

Violations shall:


Be Logged

Be Monitored

Be Reported Through Data Quality Framework


---

## Escalation

Repeated violations shall be escalated to the respective source system owner.

---

# Section Status

Section 11: Data Contracts

Status: APPROVED AND FROZEN

Version: 1.0


---

## Analytics Artifacts:

## Analytical Entities

### Forecast

Represents predictive outputs generated by forecasting models.

Examples include:

* Revenue Forecast
* Churn Forecast
* Customer Growth Forecast

### Business Description

Represents predictive outputs generated by forecasting models.

### Business Key


forecast_id


### Attributes


forecast_id
forecast_name
forecast_type
forecast_status

forecast_generation_date

forecast_period_start_date
forecast_period_end_date

predicted_value
confidence_score

model_name
model_version

created_timestamp
updated_timestamp


### Relationships


Forecast
│
└── Tenant