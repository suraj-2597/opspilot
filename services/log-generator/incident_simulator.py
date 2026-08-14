import json
import time
import psycopg2


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "opspilot",
    "user": "opspilot",
    "password": "opspilot",
}


SERVICES = {
    "checkout-service": 1,
    "order-service": 2,
    "payment-service": 3,
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def write_log(service, level, message, metadata=None):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO logs
        (service_id, level, message, metadata)
        VALUES (%s, %s, %s, %s)
        """,
        (
            SERVICES[service],
            level,
            message,
            json.dumps(metadata or {}),
        ),
    )

    connection.commit()
    cursor.close()
    connection.close()


def database_failure():
    print("🔥 Starting DATABASE_FAILURE scenario")

    write_log(
        "order-service",
        "WARN",
        "Database query latency increased",
        {"latency_ms": 820},
    )

    time.sleep(2)

    write_log(
        "order-service",
        "WARN",
        "Database connection pool utilization high",
        {"pool_utilization": 82},
    )

    time.sleep(2)

    write_log(
        "order-service",
        "WARN",
        "Database connection pool utilization critical",
        {"pool_utilization": 96},
    )

    time.sleep(2)

    write_log(
        "order-service",
        "ERROR",
        "Database connection timeout",
        {"timeout_ms": 5000},
    )

    time.sleep(2)

    write_log(
        "checkout-service",
        "ERROR",
        "Order lookup failed",
        {"dependency": "order-service"},
    )

    time.sleep(2)

    write_log(
        "checkout-service",
        "ERROR",
        "Checkout request failed",
        {"error": "ORDER_SERVICE_UNAVAILABLE"},
    )

    print("🔥 DATABASE_FAILURE scenario completed")


def main():
    print("OpsPilot Incident Simulator")
    print()
    print("Available scenarios:")
    print("1. database_failure")
    print()

    scenario = input("Enter scenario: ").strip()

    if scenario == "database_failure":
        database_failure()
    else:
        print("Unknown scenario")


if __name__ == "__main__":
    main()
