# 🤖 IT Ticket Automation Bot — Project 1

## Docker from scratch

Containerized Python/Flask agent exposing a REST API for IT ticket management.

### Endpoints

| Route | Description |
|-------|-------------|
| `GET /` | App info |
| `GET /health` | Healthcheck (status, hostname, timestamp) |
| `GET /tickets` | List of IT tickets |

### Getting started

```bash
# Build the image
docker build -t ticket-bot:v1 .

# Run the container
docker run -d -p 5000:5000 --name ticket-bot ticket-bot:v1

# Test the endpoints
curl http://localhost:5000/
curl http://localhost:5000/health
curl http://localhost:5000/tickets

# View logs
docker logs ticket-bot

# Shell into the container
docker exec -it ticket-bot /bin/sh

# Stop and remove
docker stop ticket-bot && docker rm ticket-bot
```

### Tech stack

- Python 3.11
- Flask
- Docker

### Author

Jordan Cohen — DevOps Learning Path
