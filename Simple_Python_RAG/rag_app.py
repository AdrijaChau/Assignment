import os
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from openai import OpenAI

# ==========================================
# 1. LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError(
        "OpenRouter API key not found. Please check your .env file."
    )

# ==========================================
# 2. CONNECT TO OPENROUTER
# ==========================================

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

print("OpenRouter connected successfully!")

# ==========================================
# 3. LOAD EMBEDDING MODEL
# ==========================================

print("Loading embedding model...")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded successfully!")

# ==========================================
# 4. CONNECT TO CHROMADB
# ==========================================

db_path = os.path.join(os.path.dirname(__file__), "chroma_db")

chroma_client = chromadb.PersistentClient(path=db_path)

collection = chroma_client.get_collection(
    name="company_documents"
)

print("Connected to ChromaDB successfully!")
print("Total stored chunks:", collection.count())


# ==========================================
# 5. RETRIEVE RELEVANT DOCUMENTS
# ==========================================

def retrieve_documents(question):
    # Convert question into an embedding
    question_embedding = embedding_model.encode(question).tolist()

    # Search for the 3 most relevant chunks
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=3
    )

    # Extract retrieved chunks
    retrieved_chunks = results["documents"][0]

    return retrieved_chunks


# ==========================================
# 6. GENERATE ANSWER USING LLM
# ==========================================

def generate_answer(question, retrieved_chunks):
    # Combine retrieved chunks
    context = "\n\n".join(retrieved_chunks)

    # Prepare prompt
    prompt = f"""
    You are a helpful company information assistant.

    Answer the user's question using ONLY the information
    provided in the context below.

    If the answer is not available in the context,
    clearly say that the information is not available
    in the provided documents.

    Context:
    {context}

    User Question:
    {question}

    Answer:
    """

    # Send request to OpenRouter
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    # Extract generated answer
    answer = response.choices[0].message.content

    return answer


# ==========================================
# 7. MAIN RAG APPLICATION
# ==========================================

def main():
    print("\n====================================")
    print("     COMPANY DOCUMENT RAG SYSTEM")
    print("====================================")

    print("\nYou can now ask questions about your company documents.")
    print("Type 'exit' to stop the application.")

    while True:

        question = input("\nEnter your question: ").strip()

        # Stop application if user types exit
        if question.lower() == "exit":
            print("\nThank you for using the RAG application!")
            break

        if not question:
            print("Please enter a valid question.")
            continue

        # Step 1: Retrieve relevant chunks
        print("\nSearching relevant documents...")

        retrieved_chunks = retrieve_documents(question)

        if not retrieved_chunks:
            print("No relevant information found.")
            continue

        # Step 2: Generate answer
        print("Generating answer using LLM...")

        answer = generate_answer(question, retrieved_chunks)

        # Step 3: Display answer
        print("\n====================================")
        print("ANSWER:")
        print("====================================")
        print(answer)


# ==========================================
# 8. RUN APPLICATION
# ==========================================

if __name__ == "__main__":
    main()
