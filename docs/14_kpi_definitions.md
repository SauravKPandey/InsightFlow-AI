# KPI Definitions

## Document Information

Version: 1.0

Status: Approved

Owner: Product & Analytics Team

---

# Purpose

This document defines the Key Performance Indicators (KPIs) used across InsightFlow AI.

The KPI Definitions document serves as the authoritative source for all business metric calculations across dashboards, reports, APIs, ML models, forecasting models, and Agentic AI capabilities.

---

# KPI Definition Template

Each KPI shall contain the following sections:

## KPI ID

Unique identifier for the KPI.

## KPI Name

Business-friendly KPI name.

## Business Definition

Business meaning of the KPI.

## Business Purpose

Why the KPI exists and how stakeholders use it.

## Calculation Logic

Formula or logic used to calculate the KPI.

## Business Rules

Inclusion and exclusion criteria.

Examples:

* Include ACTIVE subscriptions
* Exclude FREE subscriptions
* Exclude TRIAL subscriptions
* Include or Exclude GRACE_PERIOD subscriptions

## Business Owner

Business stakeholder responsible for the KPI.

Examples:

* CFO
* CEO
* Revenue Operations
* Product Team
* Customer Success

## Source Entities

Business entities used to calculate the KPI.

Examples:

* Subscription
* Payment
* Customer Account
* Product
* Usage Event

## Refresh Frequency

Examples:

* Real-Time
* Hourly
* Daily
* Weekly
* Monthly

## KPI Status

Possible values:

* Draft
* Approved
* Deprecated

---

# KPI Categories

## Revenue Intelligence KPIs

KPI-001 Monthly Recurring Revenue (MRR)

KPI-002 Annual Recurring Revenue (ARR)

KPI-003 Revenue by Product

KPI-004 Revenue by Product Category

KPI-005 Revenue by Geography

KPI-006 Revenue Growth %

---

## Subscription Lifecycle Intelligence KPIs

KPI-007 New Subscriptions

KPI-008 Renewed Subscriptions

KPI-009 Cancelled Subscriptions

KPI-010 Active Subscriptions

KPI-011 Grace Period Subscriptions

KPI-012 Expired Subscriptions

---

## Product Adoption Intelligence KPIs

KPI-013 Daily Active Users (DAU)

KPI-014 Monthly Active Users (MAU)

KPI-015 Feature Adoption Rate

KPI-016 Seat Utilization

KPI-017 Most Used Features

---

## Customer Health Intelligence KPIs

KPI-018 Customer Health Score

KPI-019 Healthy Customers

KPI-020 At-Risk Customers

KPI-021 Customer Tenure

---

## Churn Intelligence KPIs

KPI-022 Customer Churn Rate

KPI-023 Gross Revenue Churn

KPI-024 Net Revenue Churn

KPI-025 Churn by Product

---

## Predictive Intelligence KPIs

KPI-026 Forecasted Revenue

KPI-027 Forecasted Churn

KPI-028 At-Risk Revenue

---

## Executive Intelligence KPIs

KPI-029 Executive Revenue Scorecard

KPI-030 Executive Customer Scorecard

KPI-031 Product Penetration Rate

---

# KPI Governance Principles

## Principle 1

Business Definition and Calculation Logic are separate concepts.

A KPI may retain the same business meaning while its calculation logic evolves.

---

## Principle 2

Business Rules must be explicitly documented.

All inclusion and exclusion criteria shall be clearly defined.

---

## Principle 3

Any KPI calculation change requires:

* Decision Log Entry
* Version Update
* Stakeholder Approval

---

## Principle 4

KPI Definitions are the source of truth.

If dashboards, reports, APIs, ML models, or Agentic AI implementations conflict with KPI Definitions, the KPI Definitions document shall take precedence.

---

# Example KPI Definition

## KPI-001

### KPI Name

Monthly Recurring Revenue (MRR)

### Business Definition

Monthly recurring revenue generated from recurring subscriptions.

### Business Purpose

Provides visibility into the recurring revenue base of the business and serves as a leading indicator of business growth.

### Calculation Logic

MRR = Sum of subscription revenue normalized to monthly value.

Examples:

Monthly Plan:
₹100/month = ₹100 MRR

Quarterly Plan:
₹300/quarter = ₹100 MRR

Annual Plan:
₹1200/year = ₹100 MRR

### Business Rules

Include:

* ACTIVE subscriptions

Exclude:

* FREE subscriptions
* TRIAL subscriptions
* CANCELLED subscriptions
* EXPIRED subscriptions

GRACE_PERIOD inclusion to be defined by business policy.

### Business Owner

CFO

### Source Entities

Subscription

### Refresh Frequency

Daily

### KPI Status

Approved

# KPI Definitions

## Document Information

Version: 1.0

Status: Approved

Owner: Product & Analytics Team

---

# Purpose

This document defines the Key Performance Indicators (KPIs) used across InsightFlow AI.

The KPI Definitions document serves as the authoritative source for all business metric calculations across dashboards, reports, APIs, ML models, forecasting models, and Agentic AI capabilities.

---

# KPI Definition Template

Each KPI shall contain the following sections:

* KPI ID
* KPI Name
* Business Definition
* Business Purpose
* Calculation Logic
* Business Rules
* Business Owner
* Source Entities
* Refresh Frequency
* KPI Status

---

# Revenue Intelligence KPIs

| KPI ID  | KPI Name                        | Business Owner |
| ------- | ------------------------------- | -------------- |
| KPI-001 | Monthly Recurring Revenue (MRR) | CFO            |
| KPI-002 | Annual Recurring Revenue (ARR)  | CFO            |
| KPI-003 | Revenue by Product              | CFO            |
| KPI-004 | Revenue by Product Category     | CFO, CEO       |
| KPI-005 | Revenue by Geography            | CFO            |
| KPI-006 | Revenue Growth %                | CFO, CEO       |

---

# Subscription Lifecycle Intelligence KPIs

| KPI ID  | KPI Name                   | Business Owner     |
| ------- | -------------------------- | ------------------ |
| KPI-007 | New Subscriptions          | Revenue Operations |
| KPI-008 | Renewed Subscriptions      | Revenue Operations |
| KPI-009 | Cancelled Subscriptions    | Revenue Operations |
| KPI-010 | Active Subscriptions       | Revenue Operations |
| KPI-011 | Grace Period Subscriptions | Revenue Operations |
| KPI-012 | Expired Subscriptions      | Revenue Operations |

---

# Product Adoption Intelligence KPIs

| KPI ID  | KPI Name                   | Business Owner |
| ------- | -------------------------- | -------------- |
| KPI-013 | Daily Active Users (DAU)   | Product Team   |
| KPI-014 | Monthly Active Users (MAU) | Product Team   |
| KPI-015 | Feature Adoption Rate      | Product Team   |
| KPI-016 | Seat Utilization           | Product Team   |
| KPI-017 | Most Used Features         | Product Team   |

---

# Customer Health Intelligence KPIs

| KPI ID  | KPI Name              | Business Owner   |
| ------- | --------------------- | ---------------- |
| KPI-018 | Customer Health Score | Customer Success |
| KPI-019 | Healthy Customers     | Customer Success |
| KPI-020 | At-Risk Customers     | Customer Success |
| KPI-021 | Customer Tenure       | Customer Success |

---

# Churn Intelligence KPIs

| KPI ID  | KPI Name            | Business Owner   |
| ------- | ------------------- | ---------------- |
| KPI-022 | Customer Churn Rate | Customer Success |
| KPI-023 | Gross Revenue Churn | CFO              |
| KPI-024 | Net Revenue Churn   | CFO              |
| KPI-025 | Churn by Product    | Product Team     |

---

# Predictive Intelligence KPIs

| KPI ID  | KPI Name           | Business Owner   |
| ------- | ------------------ | ---------------- |
| KPI-026 | Forecasted Revenue | CFO              |
| KPI-027 | Forecasted Churn   | Customer Success |
| KPI-028 | At-Risk Revenue    | CFO              |

---

# Executive Intelligence KPIs

| KPI ID  | KPI Name                     | Business Owner |
| ------- | ---------------------------- | -------------- |
| KPI-029 | Executive Revenue Scorecard  | CEO            |
| KPI-030 | Executive Customer Scorecard | CEO            |
| KPI-031 | Product Penetration Rate     | CEO            |

---

# KPI Governance Principles

## Principle 1

Business Definition and Calculation Logic are separate concepts.

A KPI may retain the same business meaning while its calculation logic evolves.

---

## Principle 2

Business Rules must be explicitly documented.

All inclusion and exclusion criteria shall be clearly defined.

Examples:

* Include ACTIVE subscriptions
* Exclude FREE subscriptions
* Exclude TRIAL subscriptions
* Include or Exclude GRACE_PERIOD subscriptions

---

## Principle 3

Any KPI calculation change requires:

* Decision Log Entry
* Version Update
* Stakeholder Approval

---

## Principle 4

KPI Definitions are the source of truth.

If dashboards, reports, APIs, ML models, or Agentic AI implementations conflict with KPI Definitions, the KPI Definitions document shall take precedence.

---

# Example KPI Definition

## KPI-001

### KPI Name

Monthly Recurring Revenue (MRR)

### Business Definition

Monthly recurring revenue generated from recurring subscriptions.

### Business Purpose

Provides visibility into the recurring revenue base of the business and serves as a leading indicator of business growth.

### Calculation Logic

MRR = Sum of subscription revenue normalized to monthly value.

### Business Rules

Include:

* ACTIVE subscriptions

Exclude:

* FREE subscriptions
* TRIAL subscriptions
* CANCELLED subscriptions
* EXPIRED subscriptions

GRACE_PERIOD inclusion to be defined by business policy.

### Business Owner

CFO

### Source Entities

Subscription

### Refresh Frequency

Daily

### KPI Status

Approved
