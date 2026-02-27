# IT Ticket Automation Bot — Backend
FROM python:3.11-slim

LABEL maintainer="Jordan Cohen"
LABEL description="IT Ticket Bot — Backend API"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
