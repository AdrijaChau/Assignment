import tiktoken
from pathlib import Path

print("RAG APPLICATION STARTED")

# Locate Documents folder
project_path = Path(__file__).parent
documents_path = project_path / "Documents"

# Initialize tokenizer
encoding = tiktoken.get_encoding("cl100k_base")

# Find all text files
files = list(documents_path.glob("*.txt"))

print("\nTotal documents found:", len(files))

# Read and tokenize each document
for file_path in files:
    print("\n------------------------------")
    print("FILE NAME:", file_path.name)

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    print("\nDOCUMENT CONTENT:")
    print(text)

    tokens = encoding.encode(text)

    print("\nTOTAL TOKEN COUNT:", len(tokens))

print("\nTASK 1 COMPLETED SUCCESSFULLY!")
