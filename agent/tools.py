import psycopg2
from sentence_transformers import SentenceTransformer


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "opspilot",
    "user": "opspilot",
    "password": "opspilot",
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def get_recent_logs(limit=20):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            logs.timestamp,
            services.name,
            logs.level,
            logs.message,
            logs.metadata
        FROM logs
        JOIN services
            ON logs.service_id = services.id
        ORDER BY logs.timestamp DESC
        LIMIT %s
        """,
        (limit,),
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


def get_service_health():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            services.name,
            COUNT(logs.id) AS log_count,
            COUNT(*) FILTER (
                WHERE logs.level = 'ERROR'
            ) AS error_count,
            COUNT(*) FILTER (
                WHERE logs.level = 'WARN'
            ) AS warning_count
        FROM services
        LEFT JOIN logs
            ON logs.service_id = services.id
        GROUP BY services.name
        ORDER BY error_count DESC
        """
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


def get_recent_deployments(limit=10):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            deployments.deployed_at,
            services.name,
            deployments.version,
            deployments.commit_hash
        FROM deployments
        JOIN services
            ON deployments.service_id = services.id
        ORDER BY deployments.deployed_at DESC
        LIMIT %s
        """,
        (limit,),
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


def search_knowledge(query, limit=3):
    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    embedding = model.encode(query).tolist()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            title,
            document_type,
            content,
            1 - (embedding <=> %s::vector) AS similarity
        FROM knowledge_documents
        WHERE embedding IS NOT NULL
        ORDER BY embedding <=> %s::vector
        LIMIT %s
        """,
        (
            embedding,
            embedding,
            limit,
        ),
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


if __name__ == "__main__":

    print("\n=== RECENT LOGS ===")

    for row in get_recent_logs(10):
        print(row)

    print("\n=== SERVICE HEALTH ===")

    for row in get_service_health():
        print(row)

    print("\n=== RECENT DEPLOYMENTS ===")

    for row in get_recent_deployments(10):
        print(row)

    print("\n=== KNOWLEDGE SEARCH ===")

    results = search_knowledge(
        "checkout failures caused by database connection problems"
    )

    for row in results:
        print(
            row[0],
            "| similarity:",
            round(row[3], 3)
        )
