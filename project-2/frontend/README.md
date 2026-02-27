# 🤖 IT Ticket Automation Bot — Project 2

## Multi-container with Docker Compose

Full-stack IT ticket management system with 4 containers orchestrated by Docker Compose.

### Architecture

```
┌────────────┐     ┌─────────────┐     ┌────────────┐
│  Frontend   │────▶│   Backend   │────▶│ PostgreSQL │
│  (Nginx)    │     │   (Flask)   │     │   (DB)     │
│  port 80    │     │  port 5000  │     │  port 5432 │
└────────────┘     └──────┬──────┘     └────────────┘
                          │
                   ┌──────▼──────┐
                   │    Redis    │
                   │   (Cache)   │
                   │  port 6379  │
                   └─────────────┘
```

### Services

| Service | Image | Purpose |
|---------|-------|---------|
| frontend | Nginx Alpine | Serves HTML dashboard, proxies API calls |
| backend | Python 3.11 Flask | REST API for ticket management |
| db | PostgreSQL 16 | Persistent ticket storage |
| redis | Redis 7 Alpine | Response caching (30s TTL) |

### Getting started

```bash
# Start all services
docker compose up --build

# Or run in background
docker compose up --build -d

# Check status
docker compose ps

# View logs
docker compose logs -f backend

# Test the API directly
curl http://localhost:5000/health
curl http://localhost:5000/tickets

# Create a ticket via API
curl -X POST http://localhost:5000/tickets \
  -H "Content-Type: application/json" \
  -d '{"title": "Test ticket", "priority": "high"}'

# Open the dashboard
# http://localhost in your browser

# Stop everything
docker compose down

# Stop and remove volumes (resets database)
docker compose down -v
```

### API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | App info |
| GET | `/health` | Healthcheck (DB + Redis status) |
| GET | `/tickets` | List all tickets (cached) |
| POST | `/tickets` | Create a new ticket |
| GET | `/tickets/<id>` | Get a single ticket |

### Key concepts

- **Docker Compose** orchestrates multiple containers
- **Healthchecks** ensure services start in the right order
- **Volumes** persist database data across restarts
- **Environment variables** keep secrets out of code
- **Nginx reverse proxy** routes `/api/*` to the backend

### Tech stack

- Python 3.11 / Flask
- PostgreSQL 16
- Redis 7
- Nginx Alpine
- Docker Compose

### Author

Jordan Cohen — DevOps Learning Path
