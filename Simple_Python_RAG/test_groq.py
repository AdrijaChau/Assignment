import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    print("API key not found. Check your .env file.")

else:
    # Create OpenRouter client
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    # Send a test question
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": "Explain Generative AI in two simple sentences."
            }
        ],
        temperature=0.2
    )

    print("\nOPENROUTER RESPONSE:")
    print(response.choices[0].message.content)

