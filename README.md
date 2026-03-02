# 🛒 E-Commerce Microservices Architecture

Production-grade, learning-focused microservices architecture built with Django and Kubernetes.

---

## 📌 Project Overview

This project implements a **production-style e-commerce system** using a microservices architecture.

The goal is:

* Learn real-world distributed system design
* Apply Saga orchestration pattern
* Implement service-to-service authentication
* Use Kubernetes-native infrastructure
* Follow production-level best practices

This is not just a demo — it is designed to reflect real backend architecture standards.

---

# 🏗 Architecture Overview

## Core Services

* **Auth Service** – User authentication & JWT issuing
* **Product Service** – Product catalog management
* **Inventory Service** – Stock management & reservations
* **Cart Service** – User cart management (Redis-backed)
* **Order Service** – Saga orchestrator & order lifecycle
* **Payment Service** – Payment processing & event publishing

---

## 🧠 Architectural Principles

* ✅ Database per service
* ✅ No shared databases
* ✅ Orchestrator Saga pattern
* ✅ Event-driven communication
* ✅ Internal service JWT authentication
* ✅ Kubernetes-native deployment
* ✅ Observability-ready

---

# 🔄 Order Flow (Saga – Orchestrator Pattern)

1. Client creates order
2. Order Service reserves inventory
3. Order Service initiates payment
4. Payment Service publishes event
5. Order Service handles event:

   * Confirm inventory + mark PAID
   * OR release inventory + mark CANCELLED

All cross-service state changes are event-driven and idempotent.

---

# 🔐 Authentication Model

### External Authentication

* User JWT issued by Auth Service
* Validated by all services

### Internal Service Authentication

* Short-lived Service JWT
* Signed using private key
* Validated per service
* Only internal ClusterIP services allowed

---

# 📡 Communication Patterns

### Synchronous (REST)

* Cart → Product
* Order → Inventory
* Order → Payment

### Asynchronous (RabbitMQ)

* Payment → Order
* Order → Future consumers (Notification, Analytics)

---

# 🗄 Data Strategy

Each service owns its own PostgreSQL database:

* auth_db
* product_db
* inventory_db
* order_db
* payment_db

Redis is used for:

* Cart storage
* Caching

No cross-database joins.

---

# 🚀 Technology Stack

| Layer            | Technology   |
| ---------------- | ------------ |
| Backend          | Django + DRF |
| Database         | PostgreSQL   |
| Cache            | Redis        |
| Message Broker   | RabbitMQ     |
| Containerization | Docker       |
| Orchestration    | Kubernetes   |
| Metrics          | Prometheus   |
| Dashboard        | Grafana      |
| Logging          | Loki         |
| Tracing          | Jaeger       |

---

# 📦 Infrastructure Design

* Kubernetes namespaces (dev / staging / prod)
* ClusterIP services (internal only)
* NGINX Ingress as API gateway
* StatefulSets for:

  * PostgreSQL
  * Redis
  * RabbitMQ
* ConfigMaps & Secrets for configuration management
* Resource limits + HPA support

---

# 📊 Observability

Each service:

* Exposes `/metrics`
* Uses Correlation-ID header
* Sends structured logs to stdout
* Supports distributed tracing

---

# 🧪 Testing Strategy

* Unit tests (business logic)
* Integration tests (DB + APIs)
* Contract tests (event schemas)
* End-to-end order flow tests

---

# 📁 Repository Structure (Planned)

```
ecommerce/
│
├── auth-service/
├── product-service/
├── inventory-service/
├── cart-service/
├── order-service/
├── payment-service/
│
├── k8s/
├── docker/
├── helm/
└── docs/
```

---

# 🎯 Learning Goals

This project focuses on mastering:

* Microservice boundaries
* Saga orchestration
* Event-driven design
* Service authentication
* Distributed failure handling
* Kubernetes-native architecture
* Observability in distributed systems

---

# 🔮 Future Extensions

* Notification Service
* Analytics Service
* API rate limiting
* Circuit breaker implementation
* Service mesh integration
* Polyglot microservices

---

# 📜 License

Educational / Learning project.

