# 📦 Product Microservice

The **Catalog Engine** of the e-commerce ecosystem.  
This service is designed for **high-concurrency read operations**, utilizing an **asymmetric security model** and a **stateless architecture** to ensure **sub-100ms response times** for global product discovery.

---

# 🚀 Key Architectural Milestones

## UUID-First Domain
Built with a **distributed-identity mindset**.

All `Product`, `Category`, and `ProductImage` entities use **UUIDv4 as primary keys** to:

- Prevent ID enumeration
- Support distributed systems
- Facilitate future **DDD (Domain-Driven Design)** refactors

---

## Stateless RS256 Authentication
Implements **JWTStatelessUserAuthentication**.

The service verifies identity **locally** using the **Auth Service's RSA Public Key**, eliminating **inter-service latency** during request authorization.

---

## Production-Level Redis Caching
Uses a **Cache-Aside strategy** to offload heavy read queries from PostgreSQL to memory.

Optimizations include:

- Cached **detail views**
- Cached **filtered product lists**
- **Automatic cache invalidation** via Django signals

---

## High-Scale Pagination
Optimized using **Cursor-based Pagination** instead of traditional offsets.

Benefits:

- **O(1) performance**
- Stable results during **concurrent writes**
- Ideal for **deep pagination**

---

## Domain Integrity
Strong data integrity enforced through:

- `on_delete=models.PROTECT` for ForeignKey relations
- **Slug-based routing** for SEO-friendly and immutable resource access

---

# 🛠️ Tech Stack

| Component | Technology | Role |
|----------|-----------|------|
| Framework | Django 5.x + DRF | Core business logic |
| Auth | RS256 JWT (Stateless) | Identity verification |
| Database | PostgreSQL 15 | Persistent catalog store |
| Cache | Redis 7 | High-performance read layer |
| Pagination | Cursor-based | Deep paging stability |
| Testing | Pytest + Coverage | Quad-layer verification |

---

# 🚦 Getting Started

## 🔌 API Endpoints

| Method | Endpoint | Description | Features |
|------|------|------|------|
| GET | `/api/products/` | Catalog discovery | Filtering, Cursor paging |
| GET | `/api/products/<slug>/` | Product detail | Nested images, caching |
| GET | `/api/categories/` | Category tree | Slug-indexed |
| GET | `/health/` | Service heartbeat | DB + Redis checks |

---

# 🛠️ Development Commands (Makefile)

Standardized commands for **CI/CD and local development**.

```bash
make build    # Rebuild containers
make up       # Start Product, DB, and Redis services
make test     # Run Quad-layer test suite (Model/API/Auth/Cache)
make migrate  # Apply domain migrations


