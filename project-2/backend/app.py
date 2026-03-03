"""
IT Ticket Automation Bot — Backend API
Project 2: Multi-container with Docker Compose
"""

from flask import Flask, jsonify, request
import psycopg2
import redis
import json
import os
import datetime

app = Flask(__name__)


def get_db():
    """Database connection."""
    return psycopg2.connect(os.environ["DATABASE_URL"])


# Redis connection
cache = redis.Redis(
    host=os.environ.get("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True
)


def init_db():
    """Initialize database tables."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            priority VARCHAR(50) NOT NULL DEFAULT 'medium',
            status VARCHAR(50) NOT NULL DEFAULT 'open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("SELECT COUNT(*) FROM tickets")
    if cur.fetchone()[0] == 0:
        sample_tickets = [
            ("VPN not connecting", "high", "open"),
            ("Password reset request", "low", "open"),
            ("Disk space alert on SRV-01", "critical", "in_progress"),
            ("New laptop setup for onboarding", "medium", "open"),
            ("Email server latency issues", "high", "open"),
        ]
        cur.executemany(
            "INSERT INTO tickets (title, priority, status) "
            "VALUES (%s, %s, %s)",
            sample_tickets
        )
    conn.commit()
    cur.close()
    conn.close()


@app.route("/")
def home():
    """Home endpoint with app info."""
    return jsonify({
        "app": "IT Ticket Automation Bot",
        "version": "2.0.0",
        "author": "Jordan Cohen",
        "endpoints": ["/", "/health", "/tickets", "/tickets/<id>"]
    })


@app.route("/health")
def health():
    """Health check endpoint."""
    db_status = "healthy"
    try:
        conn = get_db()
        conn.close()
    except Exception:
        db_status = "unhealthy"

    redis_status = "healthy"
    try:
        cache.ping()
    except Exception:
        redis_status = "unhealthy"

    status = "healthy" if (
        db_status == "healthy" and redis_status == "healthy"
    ) else "degraded"

    return jsonify({
        "status": status,
        "timestamp": datetime.datetime.now().isoformat(),
        "database": db_status,
        "cache": redis_status
    })


@app.route("/tickets", methods=["GET"])
def get_tickets():
    """Get all tickets, with Redis caching."""
    cached = cache.get("tickets:all")
    if cached:
        return jsonify({
            "source": "cache",
            "tickets": json.loads(cached)
        })

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, title, priority, status, created_at "
        "FROM tickets ORDER BY id"
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    tickets = [
        {
            "id": r[0],
            "title": r[1],
            "priority": r[2],
            "status": r[3],
            "created_at": r[4].isoformat()
        }
        for r in rows
    ]

    cache.setex("tickets:all", 30, json.dumps(tickets))

    return jsonify({
        "source": "database",
        "total": len(tickets),
        "tickets": tickets
    })


@app.route("/tickets", methods=["POST"])
def create_ticket():
    """Create a new ticket."""
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "title is required"}), 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tickets (title, priority, status) "
        "VALUES (%s, %s, %s) RETURNING id",
        (
            data["title"],
            data.get("priority", "medium"),
            data.get("status", "open")
        )
    )
    ticket_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    cache.delete("tickets:all")

    return jsonify({"message": "Ticket created", "id": ticket_id}), 201


@app.route("/tickets/<int:ticket_id>", methods=["GET"])
def get_ticket(ticket_id):
    """Get a single ticket by ID."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, title, priority, status, created_at "
        "FROM tickets WHERE id = %s",
        (ticket_id,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return jsonify({"error": "Ticket not found"}), 404

    return jsonify({
        "id": row[0],
        "title": row[1],
        "priority": row[2],
        "status": row[3],
        "created_at": row[4].isoformat()
    })


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)