# Project Development Decisions

This document includes details about the implemented and skipped features during my development.

## ✅ Features Implemented

### Core Infrastructure
- **Docker Containerization**
  + Complete docker-compose.yml setup with 5 services
  + Multi-stage Dockerfile optimization
  + Health checks for all services
  + Proper service dependencies and startup order
  + Volume persistence for PostgreSQL and Redis data
  + Network segmentation (backend/frontend)
  + Structured logging with rotation policies

- **PostgreSQL Database**
  + Full Django ORM implementation
  + Proper migrations and model relationships
  + Database indexes on frequently queried fields
  + JSONField for flexible metadata storage
  + Custom model managers for common queries


- **Redis Integration**
  + Celery message broker configuration
  + Persistent data storage


### Authentication & Security
- **Strong Password Policy**
  + 8 chars minimum
  + 1 lowercase, 1 uppercase, 1 number, 1 special char
  + Cannot contain username
  + Cannot be a common password

One of my priorities as a developer is cybersecurity. Protecting users' confidentiality takes very little time for the benefit in terms of security posture.

- **JWT Authentication**
  + Access and refresh token implementation
  + Token blacklisting on logout
  + Bearer token authentication

Using JWT avoids storing sessions server-side and allows for stateless authentication, making the API more scalable.

I decided to keep the folders `apps/authentication/` and `apps/users/` separate. This way the app organization is based on functionality, as authentication and user interaction via the API serve two different purposes.

### API Implementation
- **Complete REST API**
  + All mandatory CRUD endpoints for tasks and users
  + Filtering, search, and pagination
  + Task assignment functionality
  + Comment system for tasks
  + Proper HTTP status codes and error handling

- **OpenAPI Documentation**
  + Swagger UI running on `/api/docs/`
  + Automatic schema generation
  + Interactive API testing interface

I decided to use Swagger as an additional documentation resource and, mainly, as a testing tool. Easy to setup and very useful for development and testing.

### Background Processing
- **Celery Workers**
  + Configurable concurrency (2 workers)
  + Health monitoring and status checks
  + Proper error handling and retries

- **Celery Beat Scheduler**
  + Daily summary generation task
  + Weekly cleanup of archived tasks

I implemented the core Celery infrastructure to demonstrate background processing capabilities, focusing on tasks that provide clear business value.

### Frontend Application
- **Django Templates**
  + Server-side rendered authentication (login/register)
  + Task list view with filtering
  + Task creation and detail forms
  + Navigation between pages
  + Task deletion functionality
  + Report generation and download

I decided to implement the reports generated with the frontend.

## ❌ Features Skipped

### Extended Models
- **TaskHistory Model**
  + Audit logging for task changes

I believe this added too much workload to the task for the actual benefit it brings. In addition to this, the tight deadline for the task made me prioritize other functionalities.

### Advanced Celery Tasks
- **check_overdue_tasks & send_task_notification**
  + Email notification system

I thought these tasks required actual email setting and I decided to skip it. Looking at the assignment I realized logging was enough. This feature would take no time if the goal is simply logging.

### Microservices Architecture
- **Flask & Kafka**
These two added more services and I decided to prioritize the quality of the mandatory ones.

## 🕰️ Time Allocation Breakdown

- **Day 1**: Docker infrastructure setup and Django project structure (10%)
- **Day 2**: Core API implementation and database models (20%)
- **Day 3**: Authentication system and finish API (40%)
- **Day 4**: Frontend templates (15%)
- **Day 5**: Celery, polish and documentation (15%)

## 🔧 Technical Challenges Faced

Although I had tried to code with django in the past, I never really developed an entire project with so many features in a short period of time.

I had never worked with celery either, so learning new technologies and trying to make the app work following best practices has been very time consuming.

## 🔄 Trade-offs Made

### Core services vs Microservices
I decided to prioritize the main services and submit a funcional project with a solid codebase. This allows to expand functionalities in the future easily.

### Quality vs Quantity
I decied to focus on quality instead of trying to implement as many features as possible. Detailing everything in the documentation and having a consistent application.

## 📈 What I Would Add With More Time

### Short-term
- The last 2 celery tasks
- Task editing templates
- Polish the API

### Medium-term
- Flask & Kafka microservices
- Complete frontend app with user views & admin features
- Advanced reporting and dashboard features

### Long-term
- Kubernetes deployment configuration
- AI-powered utilities
- Performance optimization and caching strategies

## 📝 Justification for Django Templates

I decided to use two different base templates:
- **auth_base.html**
    + For the login and register templates
- **task_base.html**:
    + For the tasks related templates
    + Includes a navbar

I tried to use server side rendering as much as possible, although I decided to implement the auth system in JS. This decision came because I was having problems with the default django authentication system, and I had already developed my own on the API.