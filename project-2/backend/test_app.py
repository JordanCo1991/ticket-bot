"""
IT Ticket Automation Bot — Unit Tests
Project 3: CI/CD with GitHub Actions
"""

import pytest
import json
from unittest.mock import patch, MagicMock
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home(client):
    """Test the home endpoint returns app info."""
    response = client.get("/")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["app"] == "IT Ticket Automation Bot"
    assert data["version"] == "2.0.0"
    assert data["author"] == "Jordan Cohen"
    assert "/health" in data["endpoints"]
    assert "/tickets" in data["endpoints"]


def test_home_has_all_endpoints(client):
    """Test that home lists all available endpoints."""
    response = client.get("/")
    data = json.loads(response.data)

    expected_endpoints = ["/", "/health", "/tickets", "/tickets/<id>"]
    assert data["endpoints"] == expected_endpoints


@patch("app.get_db")
@patch("app.cache")
def test_health_all_healthy(mock_cache, mock_db, client):
    """Test health endpoint when all services are up."""
    mock_conn = MagicMock()
    mock_db.return_value = mock_conn
    mock_cache.ping.return_value = True

    response = client.get("/health")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["status"] == "healthy"
    assert data["database"] == "healthy"
    assert data["cache"] == "healthy"
    assert "timestamp" in data


@patch("app.get_db")
@patch("app.cache")
def test_health_db_down(mock_cache, mock_db, client):
    """Test health endpoint when database is down."""
    mock_db.side_effect = Exception("DB connection failed")
    mock_cache.ping.return_value = True

    response = client.get("/health")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["status"] == "degraded"
    assert data["database"] == "unhealthy"
    assert data["cache"] == "healthy"


@patch("app.get_db")
@patch("app.cache")
def test_health_redis_down(mock_cache, mock_db, client):
    """Test health endpoint when Redis is down."""
    mock_conn = MagicMock()
    mock_db.return_value = mock_conn
    mock_cache.ping.side_effect = Exception("Redis connection failed")

    response = client.get("/health")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["status"] == "degraded"
    assert data["database"] == "healthy"
    assert data["cache"] == "unhealthy"


@patch("app.get_db")
@patch("app.cache")
def test_get_tickets_from_db(mock_cache, mock_db, client):
    """Test getting tickets from database when cache is empty."""
    # Cache miss
    mock_cache.get.return_value = None

    # Mock database response
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    from datetime import datetime
    mock_cursor.fetchall.return_value = [
        (1, "VPN not connecting", "high", "open", datetime(2026, 1, 1, 12, 0, 0)),
        (2, "Password reset", "low", "open", datetime(2026, 1, 1, 12, 0, 0)),
    ]
    mock_conn.cursor.return_value = mock_cursor
    mock_db.return_value = mock_conn

    response = client.get("/tickets")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["source"] == "database"
    assert data["total"] == 2
    assert len(data["tickets"]) == 2
    assert data["tickets"][0]["title"] == "VPN not connecting"


@patch("app.get_db")
@patch("app.cache")
def test_get_tickets_from_cache(mock_cache, mock_db, client):
    """Test getting tickets from Redis cache."""
    cached_tickets = [
        {"id": 1, "title": "Cached ticket", "priority": "low", "status": "open", "created_at": "2026-01-01T12:00:00"}
    ]
    mock_cache.get.return_value = json.dumps(cached_tickets)

    response = client.get("/tickets")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["source"] == "cache"
    assert data["tickets"][0]["title"] == "Cached ticket"


@patch("app.get_db")
@patch("app.cache")
def test_create_ticket_success(mock_cache, mock_db, client):
    """Test creating a new ticket."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (42,)
    mock_conn.cursor.return_value = mock_cursor
    mock_db.return_value = mock_conn

    response = client.post("/tickets",
        data=json.dumps({"title": "New server needed", "priority": "high"}),
        content_type="application/json"
    )
    data = json.loads(response.data)

    assert response.status_code == 201
    assert data["message"] == "Ticket created"
    assert data["id"] == 42
    # Verify cache was invalidated
    mock_cache.delete.assert_called_once_with("tickets:all")


@patch("app.get_db")
@patch("app.cache")
def test_create_ticket_no_title(mock_cache, mock_db, client):
    """Test creating a ticket without a title returns 400."""
    response = client.post("/tickets",
        data=json.dumps({"priority": "high"}),
        content_type="application/json"
    )
    data = json.loads(response.data)

    assert response.status_code == 400
    assert "error" in data


@patch("app.get_db")
def test_get_single_ticket(mock_db, client):
    """Test getting a single ticket by ID."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    from datetime import datetime
    mock_cursor.fetchone.return_value = (1, "VPN issue", "high", "open", datetime(2026, 1, 1, 12, 0, 0))
    mock_conn.cursor.return_value = mock_cursor
    mock_db.return_value = mock_conn

    response = client.get("/tickets/1")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["id"] == 1
    assert data["title"] == "VPN issue"


@patch("app.get_db")
def test_get_single_ticket_not_found(mock_db, client):
    """Test getting a non-existent ticket returns 404."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_conn.cursor.return_value = mock_cursor
    mock_db.return_value = mock_conn

    response = client.get("/tickets/999")
    data = json.loads(response.data)

    assert response.status_code == 404
    assert data["error"] == "Ticket not found"
