---
name: docker
description: Containerize applications with Docker. Use when you need to create Dockerfiles, docker-compose files, build images, or run containers locally.
---

# Docker

## Quick Start

### Dockerfile Template (Python/Flask)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### Dockerfile Template (Node.js)
```dockerfile
FROM node:20-slim
WORKDIR /app
COPY package*.json .
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
```

### docker-compose.yml Template
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgres://db:5432/app
    depends_on:
      - db
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: app
      POSTGRES_PASSWORD: secret
```

## Common Commands

```bash
# Build and run
docker build -t myapp .
docker run -p 5000:5000 myapp

# Compose
docker-compose up -d
docker-compose logs -f
docker-compose down

# Debug
docker exec -it container_name bash
docker logs container_name

# Cleanup
docker system prune -a
```

## Best Practices

- Use slim base images
- Multi-stage builds for production
- Don't run as root
- Use .dockerignore
- Pin versions in requirements.txt