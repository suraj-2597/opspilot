import psycopg2
from sentence_transformers import SentenceTransformer


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "opspilot",
    "user": "opspilot",
    "password": "opspilot",
}


def main():
    print("Loading embedding model...")

    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, content
        FROM knowledge_documents
        WHERE embedding IS NULL
        """
    )

    documents = cursor.fetchall()

    print(f"Found {len(documents)} documents.")

    for document_id, content in documents:

        embedding = model.encode(content).tolist()

        cursor.execute(
            """
            UPDATE knowledge_documents
            SET embedding = %s
            WHERE id = %s
            """,
            (
                embedding,
                document_id,
            ),
        )

        print(f"Embedded document {document_id}")

    connection.commit()

    cursor.close()
    connection.close()

    print("Embedding process complete.")


if __name__ == "__main__":
    main()
