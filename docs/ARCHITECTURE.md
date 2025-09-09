# Task Management System Architecture

## 🗂️ Overview

This document describes the architecture of the Enterprise Task Management System, a containerized full-stack application built with Django REST Framework, PostgreSQL, Redis, and Celery. The system provides comprehensive task management capabilities with both API and web interface access.

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client Web    │    │   API Clients   │    │  Admin Panel    │
│   Interface     │    │                 │    │                 │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────────┐
                    │  Django Server  │
                    │   (Port 8000)   │
                    └─────────┬───────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
    ┌─────▼─────┐    ┌────────▼────────┐    ┌─────▼─────┐
    │PostgreSQL │    │     Redis       │    │  Celery   │
    │Database   │    │   (Cache &      │    │ Workers   │
    │           │    │    Broker)      │    │           │
    └───────────┘    └─────────────────┘    └───────────┘
```

## 🐳 Container Architecture

The application is fully containerized using Docker Compose with the following services:

### 1. PostgreSQL Database
- **Image**: `postgres:15`
- **Purpose**: Primary data storage
- **Features**:
  - Persistent data storage via Docker volumes
  - Health checks for container readiness
  - Custom database, user, and password configuration
  - Network isolation on backend network (currently exposed to facilitate testing)

### 2. Redis Cache & Message Broker
- **Image**: `redis:7-alpine`
- **Purpose**: Caching layer and Celery message broker
- **Features**:
  - In-memory data structure store
  - Persistent storage for Celery task queue
  - Health monitoring with ping checks

### 3. Django Application Server
- **Custom Build**: Multi-stage Dockerfile
- **Purpose**: Main application server and API
- **Features**:
  - Django REST Framework API
  - Server-side rendered templates
  - Gunicorn WSGI server
  - Health checks via HTTP endpoint
  - Volume mounting for development

### 4. Celery Worker
- **Purpose**: Background task processing
- **Features**:
  - Asynchronous task execution
  - Configurable concurrency (2 workers)
  - Task monitoring and health checks
  - Shared codebase with Django app

### 5. Celery Beat Scheduler
- **Purpose**: Scheduled task management
- **Features**:
  - Periodic task scheduling
  - Daily summary generation
  - Weekly cleanup operations
  - Independent health monitoring

## 🔊 Network Architecture

### Network Segmentation
- **Backend Network**: Internal communication between services
  - PostgreSQL, Redis, Django, Celery workers
  - Bridge driver for container communication
- **Frontend Network**: External access to web services
  - Django server exposed on port 80
  - Public-facing interface

> Due to testing purposes, all services are currently exposed and belong to the backend network. This network architecture makes sense for future development and scalability _(eg: nginx reverse proxy in frontend network)_

### Port Mapping
- **Port 80**: Django web application (mapped from container port 8000)
- **Port 5432**: PostgreSQL (development access)
- **Port 6379**: Redis (development access)

> 💡 In a real production environment, only the django service would be exposed.

## 🏢 Data Architecture

### Database Design
The system uses PostgreSQL with Django ORM for data management:

#### Core Models
- **User**: Extended Django AbstractUser with team relationships
- **Task**: Central entity with rich metadata and relationships
- **Team**: User grouping and organizational structure
- **Comment**: Task-related communication
- **Tag**: Task categorization and filtering

#### Key Relationships
```
User ───────> Team
 │
 │
 ▼
Task
 │
 │
 ▼
Comment
```

### Data Persistence
- **PostgreSQL Volume**: `postgres_data` for database persistence
- **Redis Volume**: `redis_data` for cache persistence
- **Shared Volume**: `/shared` for file storage between containers

## ⚙️ Application Architecture

### Django Application Structure
```
django_backend/
├── config/
│   ├── settings.py       # Environment-based configuration
│   ├── urls.py           # URL routing
│   ├── wsgi.py
│   └── celery.py         # Celery configuration
├── apps/
│   ├── authentication/  # JWT authentication
│   ├── users/           # User management
│   ├── tasks/           # Task management
│   ├── common/          # Shared utilities
│   └── celery/          # Background tasks
└── scripts/
    └── entrypoint.sh    # Container startup script
```

### API Architecture
- **REST API**: Django REST Framework with OpenAPI documentation
- **Authentication**: JWT-based with refresh token support
- **Pagination**: Configurable page-based pagination
- **Filtering**: Query parameter-based filtering and search
- **Documentation**: Automated OpenAPI/Swagger documentation

### Frontend Architecture
The system includes a server-side rendered frontend using Django templates:

#### Template Structure
- **Authentication Templates**: Login/register forms
- **Task Management**: List, detail, and creation views
- **Reports**: Task analytics and export functionality

## 🔄 Background Processing Architecture

### Celery Task System
The application implements asynchronous processing using Celery:

#### Implemented Tasks
- **Daily Summary Generation**: Automated daily task reports
- **Archived Task Cleanup**: Periodic data maintenance

#### Scheduling
- **Celery Beat**: Periodic task scheduling
- **Redis Backend**: Task result storage and message brokering
- **Worker Scaling**: Configurable concurrency for load handling

## 🔒 Security Architecture

### Authentication & Authorization
- **JWT Tokens**: Stateless authentication with access/refresh tokens
- **Token Blacklisting**: Secure logout with token invalidation
- **Password Validation**: Custom password validators
- **Session Security**: CSRF protection and secure headers

### Network Security
- **Container Isolation**: Service separation via Docker networks
- **Environment Variables**: Sensitive configuration via .env files
- **Health Checks**: Service availability monitoring
- **Logging**: Structured logging with rotation policies
