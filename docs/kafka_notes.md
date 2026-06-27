# Kafka & CDC Working Notes (InsightFlow)

## Document Status

Status: Draft

Purpose: Capture Kafka, CDC, replay, backfill, and Bronze layer design decisions, assumptions, and learning notes before final architecture freeze.

This document is a working design artifact and is not part of the frozen architecture documentation.

---

# 1. Why Kafka?

## Business Requirements

InsightFlow requires:

* Near real-time data ingestion
* CDC support
* Multiple downstream consumers
* Replay capability
* Future streaming use cases
* Cloud portability

---

## Alternatives Considered

### Direct DB → BigQuery

#### Pros

* Simpler architecture

#### Cons

* Tight coupling between source and analytics systems
* No buffering
* No replay capability
* Difficult to support multiple consumers
* Potential data loss during outages

#### Decision

Rejected

---

### Batch File Transfer

#### Pros

* Simple implementation
* Low operational overhead

#### Cons

* Not suitable for near real-time requirements
* CDC support is difficult
* Recovery and operational overhead

#### Decision

Rejected

---

### GCP Pub/Sub

#### Pros

* Fully managed
* Native GCP integration
* Lower operational complexity

#### Cons

* Cloud-specific
* Less flexibility for future platform portability
* Less mature CDC ecosystem

#### Decision

Considered but not selected

---

### Kafka

#### Pros

* Mature CDC ecosystem
* Strong replay capability
* Event-log architecture
* Multiple downstream consumers
* Cloud agnostic
* Future-ready for streaming use cases

#### Decision

Selected

---

# 2. Kafka Mental Model

Kafka should be viewed as a distributed append-only log.

Topic
↓
Partitions
↓
Replicas
↓
Brokers

Definitions:

Topic = Logical event stream

Partition = Physical append-only log

Broker = Kafka server/node

Replication = Copies of partition logs across brokers

Cluster = Group of brokers

---

# 3. Topic Strategy

## CDC Topics

customer_topic

subscription_topic

product_topic

pricing_plan_topic

invoice_topic

payment_topic

---

## Event Topics

usage_event_topic

---

# 4. Partitioning Strategy

## Guiding Principle

Partition by the business entity whose ordering must be preserved.

---

## Partition Keys

customer_topic

customer_id

---

subscription_topic

subscription_id

---

invoice_topic

invoice_id

---

payment_topic

payment_id

---

usage_event_topic

customer_id

---

## Rationale

* Preserve ordering
* Support CDC processing
* Support replay
* Support SCD2 implementation
* Support customer-centric analytics
* Enable parallel processing

---

# 5. Ordering Guarantees

Guaranteed

* Ordering within a partition
* Ordering for same partition key

Not Guaranteed

* Ordering across partitions

---

# 6. Hot Partition Risk

Potential Risk

Large customers generating disproportionate traffic may create hot partitions.

Example

Netflix-like customer generating significantly more events than other customers.

Current Assessment

Not expected at InsightFlow scale.

Mitigation Options

* Increase partition count
* Application-level sharding
* Composite partition keys

---

# 7. Kafka Cluster Design

Current Assumptions

Brokers = 3

Replication Factor = 3

min.insync.replicas = 2

acks = all

enable.idempotence = true

---

# 8. Replication Model

Example

Partition 0

Leader Replica → Broker 1

Follower Replica → Broker 2

Follower Replica → Broker 3

Replication Factor = Total Copies

RF = 3 means:

1 Leader

2 Followers

---

# 9. Leadership Model

Leadership exists at partition level.

Broker is not the leader.

Partition replica becomes leader.

Example

Partition 0

Leader Replica → Broker 1

Partition 1

Leader Replica → Broker 2

Partition 2

Leader Replica → Broker 3

A broker can host:

* Leader replicas for some partitions
* Follower replicas for others

---

# 10. Failure Handling

Scenario

Broker 1 fails.

Before Failure

Partition 0

Leader → Broker 1

Follower → Broker 2

Follower → Broker 3

After Failure

Partition 0

Leader → Broker 2

Follower → Broker 3

Automatic leader election occurs.

No data loss occurs for acknowledged messages if replication has completed.

---

# 11. Durability Strategy

Producer Configuration

acks = all

enable.idempotence = true

Replication Factor = 3

min.insync.replicas = 2

---

## Design Goal

Favor consistency over availability.

Temporary write failures are preferred over acknowledged data loss.

---

# 12. Capacity Planning Assumptions

## Business Assumptions

Annual Active Users = 1 Million

Daily Active Users = 200,000

Daily Events = 120 Million

Average Throughput ≈ 1,400 events/sec

Peak Throughput ≈ 7,000 events/sec

---

## Consumer Throughput Assumption

Initial Estimate

≈ 2,000 events/sec per consumer

Actual throughput must be validated through load testing.

---

# 13. Partition Sizing

Required Consumers

7,000 / 2,000

≈ 4 Consumers

---

Minimum Partitions Required

4

---

Provisioned Partitions

24

---

Reason

* Future growth
* Additional consumers
* Rebalancing flexibility
* Avoid partition expansion later

---

# 14. Broker Sizing

Minimum Production Cluster

3 Brokers

Reason

Supports:

Replication Factor = 3

Provides tolerance against a single broker failure.

---

# 15. CAP Theorem

Kafka operates in a partition-tolerant distributed environment.

For durable writes Kafka favors consistency over availability.

Implication

Temporary write pauses are preferred over acknowledged data loss.

---

# 16. CDC Fundamentals

CDC = Change Data Capture

Purpose:

* Incremental processing
* Near real-time ingestion
* Minimize source database impact
* Historical change tracking
* Event-driven architecture

---

## Transaction Logs

CDC reads database transaction logs rather than source tables.

Examples:

PostgreSQL → WAL

MySQL → Binlog

Oracle → Redo Log

SQL Server → Transaction Log

---

## Why CDC?

Benefits:

* Avoid table polling
* Lower source database load
* Capture INSERT/UPDATE/DELETE events
* Support replay
* Enable downstream SCD2

CDC enables SCD2 but does not implement SCD2.

---

# 17. Snapshot Strategy

## Initial Load

When CDC is enabled:

1. Record current transaction log position
2. Take initial table snapshot
3. Start CDC from recorded position

Reason

Avoid missing updates during snapshot execution.

---

## Snapshot Events

Debezium emits:

op = r

Meaning:

Read Event

Not a true INSERT.

---

# 18. CDC Event Model

## Insert

before = null

after = populated

op = c

---

## Update

before = previous state

after = new state

op = u

---

## Delete

before = previous state

after = null

op = d

---

## Snapshot Read

before = null

after = current row state

op = r

snapshot = true

---

# 19. CDC Event Structure

Typical Event

before

after

source

op

ts_ms

---

## Source Metadata

Contains:

* Database
* Schema
* Table
* LSN
* Transaction ID

Used for:

* Auditability
* Replay
* Ordering
* Deduplication
* Recovery

---

## LSN

Think of LSN as:

Kafka Offset for the database transaction log.

Used for:

* Ordering
* Replay
* Recovery
* Deduplication

---

## Transaction ID

Used to group multiple changes occurring in the same database transaction.

---

# 20. Bronze Layer Principles

Bronze is the immutable raw event store.

Bronze stores:

* Full CDC payload
* Before image
* After image
* Operation type
* Source metadata
* Event timestamp
* Ingestion timestamp

Bronze performs:

* No deduplication
* No SCD processing
* No business transformations

Reason:

Replayability and auditability.

---

# 21. Bronze Storage Strategy

Recommended Structure

event_id

event_time

ingestion_time

op

source_db

source_table

lsn

txid

raw_payload

---

## Why Raw Payload?

Supports:

* Schema evolution
* Replay
* Audit
* Future processing requirements

Bronze should not be tightly coupled to source schemas.

---

# 22. Time Semantics

## Event Time

When source transaction occurred.

Used for:

* SCD2
* Analytics
* Business reporting
* Event ordering

---

## Ingestion Time

When platform received the event.

Used for:

* SLA monitoring
* Latency measurement
* Troubleshooting
* Observability

---

Latency Formula

Latency = Ingestion Time - Event Time

Both timestamps must be preserved.

---

# 23. Delivery Guarantees

Expected Delivery Model

At-Least-Once

Duplicates are expected.

Reason:

Distributed systems prefer duplicate events over lost events.

---

# 24. Deduplication Strategy

Deduplication occurs in Silver.

Not Bronze.

Reason:

Bronze must preserve source truth.

---

Potential Deduplication Keys

source_table

*

lsn

Reason:

LSN identifies the change event rather than the business entity.

---

# 25. Replay Strategy

Definition

Replay = Reprocessing data already present in Bronze.

Examples:

* Silver rebuild
* Gold rebuild
* Schema change
* Logic correction
* SCD2 rebuild

Source

Bronze

↓

Silver

↓

Gold

Bronze is the System of Record.

---

# 26. Backfill Strategy

Definition

Backfill = Loading historical data not present in Bronze.

Examples:

* Historical migrations
* CDC outage recovery
* New analytical requirements

---

## Approach

Convert historical data into synthetic CDC events before loading into Bronze.

Reason:

Maintains a single event-processing model across the platform.

---

# 27. Schema Evolution Principles

## Bronze

Always accept incoming CDC payloads.

Schema changes should never block Bronze ingestion.

---

## Silver

Validate schema compatibility.

---

Compatible Changes

Examples:

* New columns
* Optional fields

Action:

Continue processing

Raise alert

---

Breaking Changes

Examples:

* Column removal
* Column rename
* Data type change

Action:

DLQ

Alert

Manual review

---

# 28. InsightFlow Architecture Alignment

Architecture Style

Modern ELT

Source DB
↓
CDC
↓
Kafka
↓
GCS Bronze
↓
BigQuery Silver
↓
BigQuery Gold

Reason

Data is loaded first and transformed later.

Business transformations occur in Silver and Gold.

---

# 29. Open Questions

1. Topic retention strategy

2. Topic naming conventions

3. Schema Registry adoption

4. Avro vs Protobuf selection

5. DLQ topic strategy

6. Consumer group design

7. Log compaction requirements

8. Monitoring and observability framework

9. Schema compatibility policies

10. Final replay operational procedures

---
# Schema Registry Strategy

Purpose

Provide centralized schema versioning, schema storage, and compatibility validation.

Responsibilities

- Store schema versions
- Maintain schema history
- Validate compatibility rules
- Provide schemas to producers and consumers
- Prevent breaking schema changes from entering the platform

Non-Responsibilities

Schema Registry does not:

- Update downstream tables
- Update ETL logic
- Update dashboards
- Guarantee consumer compatibility

It validates schema compatibility, not consumer implementation correctness.

---

Compatibility Mode

Selected Mode:

BACKWARD

Reason:

Allows producers to evolve schemas while maintaining compatibility with existing consumers.

Allowed Changes

- Add optional fields
- Add nullable columns

Rejected Changes

- Remove fields
- Rename fields
- Incompatible data type changes

---

Schema Evolution Workflow

Producer
↓
Schema Registry Validation
↓
Schema Registration
↓
Kafka Publish

Compatible changes are accepted.

Breaking changes are rejected.
---

# Data Contract Strategy

Purpose

Define responsibilities and expectations between data producers and consumers.

A data contract includes:

- Topic ownership
- Schema definition
- Primary keys
- Partitioning keys
- Retention policies
- SLAs
- Compatibility policies
- Change management process

---

Ownership Model

Producer Team

Owns:

- Source schema
- Event definitions
- Event quality

Platform Team

Owns:

- CDC ingestion
- Kafka platform
- Schema Registry
- Bronze ingestion

Consumer Teams

Own:

- Downstream processing logic
- Consumer compatibility

---

Change Management

Compatible Changes

Examples:

- New optional columns
- Additional nullable fields

Action:

- Allowed
- Alert generated
- Consumer teams notified

---

Breaking Changes

Examples:

- Column removal
- Column rename
- Data type change

Action:

- Review required
- Coordination required
- Potential contract update

---

InsightFlow Principle

Producers may introduce backward-compatible changes without blocking the platform.

Breaking changes require coordination between producers and consumers.
---
# Consumer Group Design

Consumers subscribe to topics, not partitions.

Kafka automatically assigns partitions to consumers within a consumer group.

Rules

- One partition may only be assigned to one active consumer within a consumer group.
- Multiple consumer groups may independently consume the same topic.
- Maximum consumer parallelism equals the number of partitions.

Example

customer_topic

P1
P2
P3
P4

analytics_group

Consumer A → P1, P2

Consumer B → P3, P4

The consumer group collectively consumes all topic partitions.
---
# Schema Evolution Principles

Bronze Layer

- Always ingest events
- Schema changes should never block Bronze ingestion
- Preserve raw payload

Silver Layer

Validate schema compatibility.

Compatible Changes

- Add columns
- Add optional attributes

Action

- Continue processing
- Generate alert

Breaking Changes

- Remove columns
- Rename columns
- Incompatible type changes

Action

- Alert
- DLQ
- Manual review

---

Important Principle

Schema compatibility does not guarantee consumer compatibility.

Schema Registry validates schemas, not consumer implementations.


---

# 30. Freeze Criteria

Kafka & CDC design can be considered frozen after completion of:

* Schema Evolution Strategy
* Schema Registry Design
* Avro vs Protobuf Evaluation
* Consumer Design
* DLQ Design
* Replay Operations
* Monitoring Strategy
* Data Contracts


