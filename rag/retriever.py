import psycopg2
from sentence_transformers import SentenceTransformer


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "opspilot",
    "user": "opspilot",
    "password": "opspilot",
}


def search_knowledge(query, limit=3):

    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    query_embedding = model.encode(query).tolist()

    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
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
            query_embedding,
            query_embedding,
            limit,
        ),
    )

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results


if __name__ == "__main__":

    query = input(
        "Describe the production problem: "
    )

    results = search_knowledge(query)

    print("\nRelevant knowledge:\n")

    for (
        document_id,
        title,
        document_type,
        content,
        similarity,
    ) in results:

        print("=" * 70)
        print(f"Title: {title}")
        print(f"Type: {document_type}")
        print(f"Similarity: {similarity:.3f}")
        print()
        print(content.strip())
        print()
