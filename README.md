# Task Management System

## Quick Start

```
bash
git clone https://github.com/apena-ba/task-management-system.git
cd task-management-system
cp .env.sample .env
docker-compose up
docker compose down --volumes --rmi all
```

```
docker exec -it django bash
python3 manage.py createsuperuser
```
 