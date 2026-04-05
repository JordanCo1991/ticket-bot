# 🤖 IT Ticket Automation Bot

A full-stack IT ticket management system built as a DevOps learning project, demonstrating containerization, CI/CD, cloud deployment, Infrastructure as Code, and monitoring.

**Live demo:** Deployed on AWS EC2 (spun up on request)

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│   GitHub     │────▶│GitHub Actions│────▶│   AWS ECR     │
│   (Code)     │     │  (CI/CD)     │     │  (Images)     │
└─────────────┘     └──────────────┘     └──────┬───────┘
                                                 │
                    ┌──────────────┐              │
                    │  Terraform   │──────────────┤
                    │   (IaC)      │              │
                    └──────┬───────┘              │
                           │                      │
              ┌────────────▼──────────────────────▼────┐
              │              AWS Cloud                  │
              │                                        │
              │  ┌──────────┐  ┌──────────────────┐   │
              │  │   EC2     │  │      RDS          │   │
              │  │          │  │   (PostgreSQL)     │   │
              │  │ ┌──────┐ │  └──────────────────┘   │
              │  │ │Nginx │ │                          │
              │  │ │Flask │ │  ┌──────────────────┐   │
              │  │ │Redis │ │  │       S3          │   │
              │  │ └──────┘ │  │   (Storage)       │   │
              │  │          │  └──────────────────┘   │
              │  │ ┌──────┐ │                          │
              │  │ │Prom. │ │                          │
              │  │ │Graf. │ │                          │
              │  │ └──────┘ │                          │
              │  └──────────┘                          │
              └────────────────────────────────────────┘
```

## Tech Stack

| Category | Technology |
|----------|-----------|
| **Backend** | Python 3.11, Flask |
| **Database** | PostgreSQL 16 (AWS RDS) |
| **Cache** | Redis 7 |
| **Frontend** | Nginx, HTML/CSS/JS |
| **Containerization** | Docker, Docker Compose |
| **CI/CD** | GitHub Actions |
| **Cloud** | AWS (EC2, RDS, S3, ECR, IAM) |
| **IaC** | Terraform |
| **Monitoring** | Prometheus, Grafana |

## Project Structure

```
devops-project/
├── .github/workflows/
│   ├── ci.yml              # CI: lint, test, build on PR
│   └── cd.yml              # CD: build, push to ECR, deploy to EC2
├── project-1/              # Docker basics
│   ├── app.py
│   ├── Dockerfile
│   └── README.md
├── project-2/              # Multi-container with Docker Compose
│   ├── backend/
│   │   ├── app.py          # Flask API with PostgreSQL + Redis
│   │   ├── test_app.py     # 12 unit tests
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── frontend/
│   │   ├── index.html      # Dashboard UI
│   │   ├── nginx.conf      # Reverse proxy config
│   │   └── Dockerfile
│   ├── docker-compose.yml
│   └── README.md
├── terraform/              # Infrastructure as Code
│   ├── main.tf             # EC2, RDS, S3, ECR, Security Groups
│   ├── variables.tf
│   └── outputs.tf
└── README.md
```

## Features

- **REST API** with CRUD operations for IT tickets
- **Redis caching** with 30s TTL and automatic cache invalidation
- **Health checks** monitoring database and cache connectivity
- **Dark mode dashboard** with real-time auto-refresh
- **12 unit tests** with mocked database and cache layers
- **Automated CI/CD** — push to GitHub triggers tests, build, and deployment
- **Infrastructure as Code** — entire AWS setup reproducible with `terraform apply`
- **Monitoring** — Prometheus metrics collection + Grafana dashboards

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | App info and available endpoints |
| GET | `/health` | Health check (DB + Redis status) |
| GET | `/tickets` | List all tickets (cached) |
| POST | `/tickets` | Create a new ticket |
| GET | `/tickets/<id>` | Get a single ticket |
| GET | `/metrics` | Prometheus metrics |

## Getting Started

### Run locally with Docker Compose

```bash
cd project-2/
docker compose up --build
# Dashboard: http://localhost
# API: http://localhost:5000
```

### Deploy infrastructure with Terraform

```bash
cd terraform/
terraform init
terraform plan
terraform apply
```

### CI/CD Pipeline

Every push triggers the following automated pipeline:

1. **Pull Request** → CI runs linting (flake8) + unit tests (pytest) + Docker build
2. **Merge to main** → CD builds image, pushes to AWS ECR, deploys to EC2 via SSH

## Learning Journey

| Phase | Focus | Key Skills |
|-------|-------|------------|
| Project 1 | Docker basics | Dockerfile, layers, cache, Docker Hub |
| Project 2 | Docker Compose | Multi-container, networking, volumes, health checks |
| Project 3 | CI/CD | GitHub Actions, pytest, flake8, automated deployment |
| Project 4 | AWS Cloud | EC2, RDS, S3, ECR, Security Groups, IAM |
| Final | IaC + Monitoring | Terraform, Prometheus, Grafana |

## Author

**Jordan Cohen** — Infrastructure Engineer transitioning to DevOps

- GitHub: [@JordanCo1991](https://github.com/JordanCo1991)
