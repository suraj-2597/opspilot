import random
import time
import json
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


def generate_log():
    service = random.choice(list(SERVICES.keys()))

    scenarios = [
        ("INFO", "Request completed successfully"),
        ("INFO", "Request received"),
        ("INFO", "Database query completed"),
        ("INFO", "External service response received"),
        ("WARN", "Request latency slightly elevated"),
    ]

    level, message = random.choice(scenarios)

    metadata = {
        "latency_ms": random.randint(50, 400),
        "request_id": f"req-{random.randint(10000, 99999)}",
    }

    return service, level, message, metadata


def save_log(service, level, message, metadata):
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
            json.dumps(metadata),
        ),
    )

    connection.commit()
    cursor.close()
    connection.close()


def main():
    print("OpsPilot Log Generator started...")

    while True:
        service, level, message, metadata = generate_log()

        save_log(
            service,
            level,
            message,
            metadata,
        )

        print(
            f"[{level}] "
            f"{service} - "
            f"{message} - "
            f"{metadata}"
        )

        time.sleep(2)


if __name__ == "__main__":
    main()
