"""Synthetic incident dataset for evaluation"""

INCIDENTS = [
    {
        "incident_id": "inc-001",
        "description": "Checkout service failing with 500 errors. Order service experiencing database connection timeouts.",
        "timestamp": "2024-01-15T10:30:00Z",
        "ground_truth": {
            "root_cause": "Database connection pool exhausted due to increased traffic",
            "severity": "critical",
            "affected_services": ["order-service", "checkout-service"],
            "remediation": "Increase database connection pool from 20 to 50 connections"
        },
        "evidence": {
            "logs": [
                "order-service | ERROR: Cannot get a connection, pool error Timeout waiting for idle object",
                "checkout-service | ERROR: Request to order-service timeout after 30s",
                "database-logs | Connection pool exhausted at 10:28:00"
            ],
            "metrics": {
                "order_service_error_rate": "45%",
                "database_cpu": "92%",
                "database_connections": "20/20 (100%)"
            },
            "recent_deployments": [
                "order-service v2.3.1 deployed 2 hours ago"
            ]
        }
    },
    {
        "incident_id": "inc-002",
        "description": "Payment service requests are slow. Affecting checkout completion.",
        "timestamp": "2024-01-15T14:00:00Z",
        "ground_truth": {
            "root_cause": "Payment gateway API experiencing degradation",
            "severity": "high",
            "affected_services": ["payment-service"],
            "remediation": "Failover to backup payment gateway provider"
        },
        "evidence": {
            "logs": [
                "payment-service | Payment gateway latency: 5000ms (normal: 200ms)",
                "payment-service | Request queue depth: 500 (normal: 10)"
            ],
            "metrics": {
                "payment_service_p99_latency": "5500ms",
                "payment_gateway_status": "degraded"
            },
            "recent_deployments": []
        }
    },
    {
        "incident_id": "inc-003",
        "description": "User notifications are delayed. Users reporting not receiving order confirmations.",
        "timestamp": "2024-01-16T08:15:00Z",
        "ground_truth": {
            "root_cause": "Message queue backed up due to slow consumer",
            "severity": "medium",
            "affected_services": ["notification-service"],
            "remediation": "Scale notification service from 2 to 5 replicas"
        },
        "evidence": {
            "logs": [
                "notification-service | Message queue lag: 50000 messages (normal: 100)",
                "kafka | Consumer group notification-group lag: 50000"
            ],
            "metrics": {
                "notification_queue_depth": 50000,
                "notification_service_cpu": "98%"
            },
            "recent_deployments": [
                "notification-service v1.2.0 deployed 6 hours ago with new template rendering"
            ]
        }
    }
]

def get_incident(incident_id):
    for incident in INCIDENTS:
        if incident["incident_id"] == incident_id:
            return incident
    return None

def list_incidents():
    return [inc["incident_id"] for inc in INCIDENTS]
