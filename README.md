# E-commerce Backend (Microservices Architecture)

A production-ready E-commerce backend system built with **Django** and **Django REST Framework**, following **microservices architecture** and real-world backend engineering best practices.

This project is designed to simulate how modern backend systems are built in professional environments, focusing on **scalability, performance, security, and maintainability**.

## Key Features

- Microservices-based architecture (service-per-domain)
- RESTful APIs using Django REST Framework
- JWT authentication and authorization
- PostgreSQL database with optimized relational modeling
- Asynchronous task processing using Celery and Redis
- Cloud-based media and file storage (S3-compatible)
- Payment integration (PayPal)
- Real-time features via WebSockets (Django Channels)
- API documentation with Swagger (drf-yasg)
- Dockerized development and deployment setup
- Production-oriented security and performance optimizations

## Architecture Overview

Each core business domain is implemented as an independent service with its own database and deployment lifecycle:

- Auth Service
- Product Service
- Cart Service
- Order Service
- Payment Service
- Notification Service

Inter-service communication is handled via REST APIs and asynchronous events.

## Purpose

This project serves as:
- A learning-focused implementation of real-world backend architecture
- A portfolio project demonstrating senior-level Django and backend engineering skills
- A foundation for extending into advanced distributed systems and cloud deployments
