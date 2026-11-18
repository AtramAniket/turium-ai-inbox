
from app.services.embedding import generate_embedding
from app.services.vector_store import collection


def retrieve_relevant_chunks(
    question: str,
    limit: int = 5
) -> list[dict]:

    total_chunks = collection.count()

    if total_chunks == 0:
        return []

    question_embedding = generate_embedding(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=min(limit, total_chunks),
        include=["documents", "metadatas", "distances"],
    )

    retrieved_chunks = []

    for document, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        retrieved_chunks.append({
            "content": document,
            "metadata": metadata,
            "distance": distance,
        })

    return retrieved_chunks
