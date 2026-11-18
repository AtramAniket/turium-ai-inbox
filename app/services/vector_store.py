import chromadb

client = chromadb.PersistentClient(
    path="./data/chroma"
)

collection = client.get_or_create_collection(
    name="knowledge_chunks",
    metadata={"hnsw:space": "cosine"},
)


def store_chunks(
    item_id: str,
    title: str,
    source_type: str,
    source_url: str | None,
    chunks: list[str],
    embeddings: list[list[float]],
) -> None:

    if not chunks:
        return

    ids = [
        f"{item_id}_{index}"
        for index in range(len(chunks))
    ]

    metadatas = [
        {
            "item_id": item_id,
            "title": title,
            "source_type": source_type,
            "source_url": source_url or "",
            "chunk_index": index,
        }
        for index in range(len(chunks))
    ]

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
    )