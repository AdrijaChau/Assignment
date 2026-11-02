import chromadb

from pathlib import Path
from sentence_transformers import SentenceTransformer

# Step 1: Locate project folder
project_path = Path(__file__).parent

# Step 2: Load embedding model
print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

# Step 3: Connect to existing ChromaDB
client = chromadb.PersistentClient(
    path=str(project_path / "chroma_db")
)

# Step 4: Access existing collection
collection = client.get_collection(
    name="company_documents"
)

print("Database connected successfully!")

# Step 5: Ask user for a question
query = input("\nEnter your question: ")

# Step 6: Convert question into embedding
query_embedding = model.encode(query).tolist()

# Step 7: Search for relevant chunks
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

# Step 8: Display search results
print("\nMOST RELEVANT DOCUMENT CHUNKS:")

for i, document in enumerate(results["documents"][0]):
    print("\nResult", i + 1)
    print("-----------------------------")

    print("Document:", document)

    print("Source:",
          results["metadatas"][0][i]["source"])

    print("Chunk Number:",
          results["metadatas"][0][i]["chunk_number"])

print("\nSIMILARITY SEARCH COMPLETED!")
