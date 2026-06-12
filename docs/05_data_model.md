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
Payment


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

```text
Customer          → CRM
Subscription      → Subscription Platform
Invoice           → Billing Platform
Payment           → Payment Gateway
Product           → MDM
Pricing Plan      → MDM
```

---

## Principle 3: Backward Compatibility

Schema changes must be communicated before implementation.

Examples:

```text
New Columns            → Allowed

Column Removal         → Approval Required

Datatype Changes       → Approval Required

Business Key Changes   → Not Allowed
```

---

## Principle 4: Mandatory Business Keys

Business keys must:

```text
Be Present

Be Unique

Be Stable

Never Be Reused
```

---

## Principle 5: Data Validation

All inbound data shall be validated against:

```text
Datatype Rules

Nullability Rules

Allowed Values

Referential Integrity Rules
```

before publication into Silver.

---

# 11.2 Enterprise Data Standards

## Business Key Standard

Datatype:

```text
STRING
```

Rules:

```text
Not Null

Unique

Immutable
```

Examples:

```text
customer_id

subscription_id

invoice_id

payment_id

product_id

plan_id
```

---

## Date Standard

Datatype:

```text
DATE
```

Format:

```text
YYYY-MM-DD
```

Example:

```text
2026-06-12
```

Applicable Fields:

```text
invoice_date

subscription_start_date

subscription_end_date
```

---

## Timestamp Standard

Datatype:

```text
TIMESTAMP
```

Timezone:

```text
UTC
```

Format:

```text
ISO-8601
```

Example:

```text
2026-06-12T14:30:25Z
```

Applicable Fields:

```text
event_timestamp

created_timestamp

updated_timestamp

payment_processed_timestamp
```

---

## Currency Standard

Datatype:

```text
NUMERIC
```

Rules:

```text
No FLOAT Usage

Precision Preserved
```

Applicable Fields:

```text
invoice_amount

payment_amount

subscription_amount

arr

mrr
```

---

## Boolean Standard

Allowed Values:

```text
TRUE

FALSE
```

Not Allowed:

```text
Y/N

1/0

Yes/No
```

---

## Status Standard

Status fields must contain approved enumerated values.

Example:

```text
subscription_status

ACTIVE
CANCELLED
EXPIRED
GRACE_PERIOD
```

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

```text
Schema Validation

Datatype Validation

Mandatory Field Validation

Referential Integrity Validation

Business Rule Validation
```

---

## Contract Violations

Contract violations shall not stop ingestion into Bronze.

Violations shall:

```text
Be Logged

Be Monitored

Be Reported Through Data Quality Framework
```

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