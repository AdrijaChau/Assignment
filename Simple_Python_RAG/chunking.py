import tiktoken
from pathlib import Path

# Locate Documents folder
project_path = Path(__file__).parent
documents_path = project_path / "Documents"

# Initialize tokenizer
encoding = tiktoken.get_encoding("cl100k_base")

# Define chunk parameters
CHUNK_SIZE = 120
CHUNK_OVERLAP = 20

# Find all text documents
files = list(documents_path.glob("*.txt"))

# Process each document
for file_path in files:

    print("\n================================")
    print("DOCUMENT:", file_path.name)
    print("================================")

    # Read document
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    # Convert text into tokens
    tokens = encoding.encode(text)

    # Create chunks
    chunks = []

    start = 0

    while start < len(tokens):
        end = start + CHUNK_SIZE

        chunk_tokens = tokens[start:end]

        chunk_text = encoding.decode(chunk_tokens)

        chunks.append(chunk_text)

        start += CHUNK_SIZE - CHUNK_OVERLAP

    # Display chunks
    print("\nTOTAL TOKENS:", len(tokens))
    print("TOTAL CHUNKS:", len(chunks))

    for i, chunk in enumerate(chunks):
        print("\nCHUNK", i + 1)
        print(chunk)
        print("TOKEN COUNT:", len(encoding.encode(chunk)))

print("\nCHUNKING COMPLETED!")
