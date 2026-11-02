import tiktoken
from pathlib import Path
from sentence_transformers import SentenceTransformer

# Locate Documents folder
project_path = Path(__file__).parent
documents_path = project_path / "Documents"

# Initialize tokenizer
encoding = tiktoken.get_encoding("cl100k_base")

# Define chunk parameters
CHUNK_SIZE = 120
CHUNK_OVERLAP = 20

# Load embedding model
print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded successfully!")

# Store all chunks
all_chunks = []

# Read documents and create chunks
for file_path in documents_path.glob("*.txt"):

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    tokens = encoding.encode(text)

    start = 0

    while start < len(tokens):
        end = start + CHUNK_SIZE

        chunk_tokens = tokens[start:end]

        chunk_text = encoding.decode(chunk_tokens)

        all_chunks.append({
            "document": file_path.name,
            "text": chunk_text
        })

        start += CHUNK_SIZE - CHUNK_OVERLAP

# Generate embeddings
print("\nGenerating embeddings...")

texts = [chunk["text"] for chunk in all_chunks]

if texts:
    embeddings = model.encode(texts)

    print("\nTotal chunks:", len(texts))
    print("Embedding shape:", embeddings.shape)

    print("\nFirst chunk:")
    print(texts[0])

    print("\nFirst embedding vector:")
    print(embeddings[0])

    print("\nEmbedding vector size:", len(embeddings[0]))

else:
    print("No chunks found!")

print("\nEMBEDDING GENERATION COMPLETED!")
