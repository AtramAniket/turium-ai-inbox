# Turium AI Knowledge Inbox

A lightweight AI-powered knowledge management backend that allows users to save notes and web pages, search their content semantically, and ask questions with answers grounded in their saved knowledge.

Built with **Python, FastAPI, SQLite, ChromaDB and OpenAI**.

## Features

- **Content ingestion:** Save plain-text notes or ingest content from URLs.
- **Web extraction:** Fetch and extract readable content from web pages.
- **Text chunking:** Split content into manageable chunks using paragraph-first chunking, with overlap for oversized paragraphs.
- **Semantic embeddings:** Generate vector embeddings using OpenAI.
- **Vector storage:** Store and persist embeddings using ChromaDB.
- **Semantic retrieval:** Retrieve relevant content based on the meaning of a question.
- **AI-powered answers:** Generate answers using retrieved context.
- **Source citations:** Return the original source, title and relevant content alongside generated answers.

## Technology Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Backend framework | FastAPI |
| Database | SQLite |
| ORM | SQLAlchemy 2.0 |
| Vector database | ChromaDB |
| Embeddings | OpenAI Embeddings API |
| Answer generation | OpenAI Chat Completions API |
| URL extraction | HTTPX, BeautifulSoup |
| Validation | Pydantic |

## Architecture

The backend separates content ingestion from question answering.

### 1. Content ingestion

When a user submits a note or URL:

1. The API receives and validates the request.
2. For URLs, the application fetches and extracts the page content.
3. The original content and its metadata are stored in SQLite.
4. The content is divided into smaller chunks.
5. OpenAI generates embeddings for those chunks.
6. Chunks, embeddings and source metadata are stored in ChromaDB.
7. The item is marked as completed once processing succeeds.

### 2. Question answering

When a user submits a question:

1. The question is converted into an embedding.
2. ChromaDB searches for semantically relevant chunks using cosine distance.
3. The retrieved chunks are supplied as context to the language model.
4. The model generates an answer grounded in the supplied context.
5. Citation references are mapped back to the retrieved source metadata.
6. The API returns the answer and citations.

### Architecture overview

```text
                   FastAPI
                      |
             +--------+--------+
             |                 |
             v                 v
         Ingestion           Query
             |                 |
       +-----+-----+           |
       |           |           v
       v           v       Question
    URL Fetch   Note Input  Embedding
       |           |           |
       +-----+-----+           v
             |             ChromaDB
             v             Retrieval
        Text Chunking          |
             |                 |
             v                 v
      OpenAI Embeddings    Retrieved Context
             |                 |
             v                 v
          ChromaDB          OpenAI LLM
             |                 |
             v                 v
       SQLite Metadata    Answer + Citations
```

SQLite stores the original content and item metadata, while ChromaDB stores searchable chunks and their embeddings.

## Project Structure

```text
turium-ai-inbox/
│
├── app/
│   ├── api/
│   │   ├── ingest.py
│   │   └── query.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── db/
│   │   ├── base.py
│   │   ├── session.py
│   │   └── init_db.py
│   │
│   ├── models/
│   │   └── item.py
│   │
│   ├── schemas/
│   │   ├── ingest.py
│   │   ├── item.py
│   │   └── query.py
│   │
│   ├── services/
│   │   ├── extraction.py
│   │   ├── chunking.py
│   │   ├── embedding.py
│   │   ├── vector_store.py
│   │   ├── ingestion.py
│   │   ├── retrieval.py
│   │   └── generation.py
│   │
│   └── main.py
│
├── data/
│   └── chroma/
│
├── .env.example
├── .gitignore
└── requirements.txt
```

## Prerequisites

Before running the application, ensure you have:

- Python 3.11 or later.
- pip.
- Git.
- An OpenAI API key with access to the selected embedding and chat models.

## Getting Started

### 1. Clone the repository

```bash
git clone <YOUR_BACKEND_REPOSITORY_URL>
cd turium-ai-inbox
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate the environment.

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the repository root.

```env
OPENAI_API_KEY=your_openai_api_key
CHAT_MODEL=your_chat_model
EMBEDDING_MODEL=your_embedding_model

DATABASE_URL=sqlite:///./knowledge_inbox.db
```

Replace the model names with models available to your OpenAI API account.

The embedding model must remain consistent between document ingestion and question retrieval.

**Important:** Never commit your `.env` file or expose your API key publicly.

### 5. Run the application

From the repository root:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

SQLite tables are initialized by the application. ChromaDB uses persistent local storage under `data/chroma/`.

## API Reference

### POST `/ingest`

Adds a note or ingests content from a URL.

**Example: Save a note**

```json
{
  "source_type": "note",
  "title": "My Notes",
  "content": "This is some information I want to save."
}
```

**Example: Ingest a URL**

```json
{
  "source_type": "url",
  "url": "https://example.com"
}
```

The endpoint extracts the content when necessary, stores the original item, generates chunks and embeddings, and saves them in ChromaDB.

### GET `/items`

Returns saved knowledge items and their metadata.

### POST `/query`

Searches the knowledge base and generates an answer using retrieved context.

**Example request**

```json
{
  "question": "What information have I saved about artificial intelligence?"
}
```

**Example response**

```json
{
  "answer": "Your saved content discusses artificial intelligence...",
  "citations": [
    {
      "title": "AI Notes",
      "item_id": "item-uuid",
      "source_url": "",
      "chunk_index": 0,
      "content": "Relevant source content..."
    }
  ]
}
```

For URL sources, citations include the original source URL. For notes, the URL is empty.

Refer to `/docs` for the exact request and response schemas implemented by the running application.

## Design Decisions and Trade-offs

### SQLite and ChromaDB

The application uses two storage systems for different responsibilities:

- SQLite stores original content, item metadata, timestamps and processing status.
- ChromaDB stores text chunks, embeddings and metadata required for semantic retrieval.

This separation keeps relational data management independent of vector search.

### Paragraph-first chunking

Content is split using paragraphs as the primary boundaries.

Smaller paragraphs are combined where possible, while oversized paragraphs are divided into smaller chunks.

Current defaults:

- Chunk size: 200 words.
- Overlap: 40 words for oversized paragraphs.

Word-based chunking was selected to keep the implementation simple for this MVP. It is not equivalent to token-based chunking.

### Similarity search

ChromaDB handles vector similarity search using cosine distance. Manual cosine similarity calculations are unnecessary because vector comparison is delegated to the vector database.

### Source-grounded generation

The language model receives retrieved content as context and is instructed to answer using that context.

Citations are mapped in Python from model-returned reference numbers to actual retrieved chunks and their metadata. This avoids relying on the model to invent source identifiers or URLs.

## AI Coding Assistance and Disclosure

An AI coding agent was used as a development aid during this project.

Its assistance included:

- Discussing implementation approaches and architectural trade-offs.
- Helping scaffold and refine parts of the application.
- Reviewing code and suggesting improvements.
- Assisting with debugging and explaining unfamiliar implementation details.
- Supporting the preparation of project documentation.

AI-generated suggestions were reviewed, adapted and tested as part of the development process. The developer remained responsible for implementation decisions, integration, verification and understanding the resulting code.

The coding agent was used as an assistant, not as a substitute for reviewing or validating the application's behaviour.

## Known Limitations

- Semantic retrieval depends on the relevance of retrieved chunks. Similarity search does not guarantee that every required fact is retrieved.
- Questions requiring numerical aggregation or comparisons across many records may need structured data extraction and deterministic queries.
- URL extraction depends on page accessibility and HTML structure. Some JavaScript-rendered or protected pages may not be extractable.
- The current chunking strategy uses word counts rather than model token counts.
- The application currently uses synchronous OpenAI and ChromaDB operations.
- SQLite and ChromaDB do not share a transaction, so failures between storage operations can result in inconsistent state.
- The application is designed as a local MVP, not a fully hardened production service.

## Production Considerations

Potential improvements for a production deployment:

- Background processing for ingestion using a task queue.
- Retry mechanisms and reconciliation for failed ingestion operations.
- More robust URL fetching and SSRF protection.
- Token-aware chunking and configurable retrieval strategies.
- Structured logging, monitoring and request tracing.
- Rate limiting and authentication.
- Managed database and persistent vector infrastructure.
- Automated tests for extraction, chunking, ingestion, retrieval and generation.
- Better handling of long-running requests and OpenAI API failures.

## License

M.I.T Licence
