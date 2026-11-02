import tiktoken
import chromadb

from pathlib import Path
from sentence_transformers import SentenceTransformer

# Step 1: Locate Documents folder
project_path = Path(__file__).parent
documents_path = project_path / "Documents"

# Step 2: Initialize tokenizer
encoding = tiktoken.get_encoding("cl100k_base")

CHUNK_SIZE = 120
CHUNK_OVERLAP = 20

# Step 3: Load embedding model
print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded successfully!")

# Step 4: Initialize ChromaDB
client = chromadb.PersistentClient(
    path=str(project_path / "chroma_db")
)

# Step 5: Create a collection
collection = client.get_or_create_collection(
    name="company_documents"
)

# Step 6: Read documents and create chunks
all_chunks = []
all_metadata = []
all_ids = []

for file_path in documents_path.glob("*.txt"):

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    tokens = encoding.encode(text)

    start = 0
    chunk_number = 1

    while start < len(tokens):
        end = start + CHUNK_SIZE
        chunk_tokens = tokens[start:end]

        chunk_text = encoding.decode(chunk_tokens)

        all_chunks.append(chunk_text)

        all_metadata.append({
            "source": file_path.name,
            "chunk_number": chunk_number
        })

        all_ids.append(
            f"{file_path.stem}_chunk_{chunk_number}"
        )

        start += CHUNK_SIZE - CHUNK_OVERLAP
        chunk_number += 1

# Step 7: Generate embeddings
print("\nGenerating embeddings...")

embeddings = model.encode(all_chunks).tolist()

# Step 8: Store data in ChromaDB
if all_chunks:

    collection.upsert(
        ids=all_ids,
        documents=all_chunks,
        embeddings=embeddings,
        metadatas=all_metadata
    )

    print("\nDocuments stored successfully!")

    print("Total chunks stored:", collection.count())

else:
    print("No document chunks found!")

print("\nCHROMADB STORAGE COMPLETED!")
