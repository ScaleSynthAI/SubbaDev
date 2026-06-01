Title: Building a job-matching pipeline with Gemini embeddings and pgvector
Date: 2026-04-20
Category: ML Systems
Slug: building-job-matching-pipeline-gemini-pgvector
Summary: A detailed technical walkthrough showing how to build a semantic search and resume matching engine using pgvector and Gemini's text-embedding-004 model.

Traditional keyword search for matching resumes to job descriptions fails to capture semantic alignment, such as mapping "AWS Engineer" to a resume highlighting "Cloud Systems Specialist (Amazon Web Services)". By leveraging dense vector representations (embeddings) and stores like `pgvector`, we can build a semantic job-matching pipeline that calculates high-fidelity similarities in milliseconds.

## Database Schema with pgvector

To support vector similarity, we first enable the `vector` extension in PostgreSQL and define a schema. Google Gemini's `text-embedding-004` model produces 768-dimensional float vectors.

```sql
-- Enable the vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Table for job postings
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    embedding VECTOR(768)
);

-- Table for resume profiles
CREATE TABLE resumes (
    id SERIAL PRIMARY KEY,
    candidate_name VARCHAR(255) NOT NULL,
    experience_summary TEXT NOT NULL,
    embedding VECTOR(768)
);
```

## Creating the HNSW Index

For production environments containing 50K+ postings (such as the architecture powering **ApplyRail**), standard linear search (sequential scan) degrades performance. We construct a Hierarchical Navigable Small World (HNSW) index to enable approximate nearest neighbor (ANN) lookups with sub-50ms response times. We use cosine distance (`vector_cosine_ops`):

```sql
CREATE INDEX jobs_hnsw_idx ON jobs 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```

## Python Implementation: Generating Embeddings

We use the Google GenAI SDK to generate embeddings for resumes and job postings:

```python
import os
import psycopg2
from google import genai
from google.genai import types

# Initialize Gemini Client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def get_gemini_embedding(text: str) -> list[float]:
    """Generate 768-dimensional text embedding."""
    response = client.models.embed_content(
        model="text-embedding-004",
        contents=text,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT"
        )
    )
    return response.embeddings[0].values

# Example usage to store a job embedding
def store_job(title: str, description: str):
    vector = get_gemini_embedding(f"{title}: {description}")
    
    conn = psycopg2.connect("dbname=applyrail user=postgres")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO jobs (title, description, embedding) VALUES (%s, %s, %s);",
        (title, description, vector)
    )
    conn.commit()
    cur.close()
    conn.close()
```

## Semantic Query Resolution

When matching a resume against all available jobs, we compute the cosine similarity ($1 - \text{cosine\_distance}$). In SQL, this is expressed using the pgvector `<=>` operator (cosine distance):

```sql
-- Find top 5 jobs matching a specific candidate's resume embedding
SELECT 
    title,
    description,
    1 - (embedding <=> %s) AS similarity_score
FROM jobs
ORDER BY embedding <=> %s
LIMIT 5;
```

This query bypasses expensive text parsing and directly queries the HNSW graph. It resolves in ~12ms on standard PostgreSQL instances running in a Docker container, providing robust, scalable search capabilities.
