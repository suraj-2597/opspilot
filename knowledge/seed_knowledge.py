import json
import psycopg2


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "opspilot",
    "user": "opspilot",
    "password": "opspilot",
}


DOCUMENTS = [
    {
        "title": "Database Connection Pool Exhaustion Runbook",
        "document_type": "runbook",
        "content": """
When database connection pool utilization exceeds 90 percent,
investigate long-running queries, connection leaks, and sudden
traffic increases.

Symptoms may include:
- Increased database latency
- Connection timeout errors
- HTTP 500 responses
- Downstream service failures

Recommended investigation:
1. Check database connection pool utilization.
2. Identify long-running queries.
3. Check recent deployments.
4. Inspect application connection handling.
5. Roll back a recent deployment if it introduced connection leaks.

A database connection failure can cause cascading failures in
services that depend on the database.
""",
        "metadata": {
            "service": "order-service",
            "category": "database"
        }
    },
    {
        "title": "Checkout Service Dependency Architecture",
        "document_type": "architecture",
        "content": """
Checkout Service depends on Order Service and Payment Service.

Request flow:

Client
  -> Checkout Service
  -> Order Service
  -> Database

Checkout failures can therefore be caused by failures in
downstream services.

When investigating checkout failures, identify the earliest
failing dependency rather than assuming checkout itself is
the root cause.
""",
        "metadata": {
            "service": "checkout-service",
            "category": "architecture"
        }
    },
    {
        "title": "Historical Incident: Order Database Timeout",
        "document_type": "incident",
        "content": """
A previous production incident caused checkout failures.

Observed symptoms:
- Checkout latency increased
- Order Service latency increased
- Database connection pool reached 96 percent
- Database connection timeouts appeared
- Checkout returned ORDER_SERVICE_UNAVAILABLE

Root cause:
Database connection exhaustion in Order Service.

Resolution:
Connections were released correctly and the problematic
deployment was rolled back.

Lesson:
The earliest database warning was a stronger root-cause signal
than the later checkout errors.
""",
        "metadata": {
            "incident_id": "INC-1042",
            "severity": "high"
        }
    }
]


def main():
    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()

    for document in DOCUMENTS:
        cursor.execute(
            """
            INSERT INTO knowledge_documents
            (title, document_type, content, metadata)
            VALUES (%s, %s, %s, %s)
            """,
            (
                document["title"],
                document["document_type"],
                document["content"],
                json.dumps(document["metadata"]),
            ),
        )

    connection.commit()

    cursor.close()
    connection.close()

    print(f"Inserted {len(DOCUMENTS)} knowledge documents.")


if __name__ == "__main__":
    main()
