"""
IT Ticket Automation Bot — Base Agent
Project 1: Docker from scratch
"""

from flask import Flask, jsonify
import platform
import datetime

app = Flask(__name__)

# Sample IT tickets to start with
SAMPLE_TICKETS = [
    {"id": 1, "title": "VPN not connecting", "priority": "high", "status": "open"},
    {"id": 2, "title": "Password reset request", "priority": "low", "status": "open"},
    {"id": 3, "title": "Disk space alert on SRV-01", "priority": "critical", "status": "in_progress"},
]


@app.route("/")
def home():
    return jsonify({
        "app": "IT Ticket Automation Bot",
        "version": "1.0.0",
        "author": "Jordan Cohen",
        "endpoints": ["/", "/health", "/tickets"]
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat(),
        "hostname": platform.node(),
        "python_version": platform.python_version()
    })


@app.route("/tickets")
def tickets():
    return jsonify({
        "total": len(SAMPLE_TICKETS),
        "tickets": SAMPLE_TICKETS
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
