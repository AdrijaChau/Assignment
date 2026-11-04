import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from tools import search_books, reserve_book

load_dotenv()

# Point OpenAI client to Groq's API endpoint
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# Define Tool Schemas (Same format as OpenAI)
tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "search_books",
            "description": "Searches the library collection for books by title, author, or category keyword.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Keyword to search for in titles, authors, or categories."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "reserve_book",
            "description": "Reserves a book for a customer given the book ID and customer name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "book_id": {
                        "type": "integer",
                        "description": "The unique ID of the book to reserve."
                    },
                    "customer_name": {
                        "type": "string",
                        "description": "Full name of the person reserving the book."
                    }
                },
                "required": ["book_id", "customer_name"]
            }
        }
    }
]


def run_agent(user_prompt: str):
    messages = [
        {"role": "system",
         "content": "You are a helpful AI Library Assistant. You search books and reserve them when requested."},
        {"role": "user", "content": user_prompt}
    ]

    # Use Llama 3.3 70B via Groq
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        tools=tools_schema,
        tool_choice="auto"
    )

    response_message = response.choices[0].message

    if response_message.tool_calls:
        tool_call = response_message.tool_calls[0]
        func_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        print(f"🤖 [Agent Decision]: Executing tool '{func_name}' with arguments: {args}")

        if func_name == "search_books":
            tool_output = search_books(args.get("query"))
        elif func_name == "reserve_book":
            tool_output = reserve_book(args.get("book_id"), args.get("customer_name"))
        else:
            tool_output = "Tool not found."

        messages.append(response_message)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": tool_output
        })

        final_response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages
        )
        print("\n💬 [Assistant Response]:")
        print(final_response.choices[0].message.content)
    else:
        print("\n💬 [Assistant Response]:")
        print(response_message.content)


if __name__ == "__main__":
    print("--- Testing Search ---")
    run_agent("Do you have any books on Python programming?")

    print("\n" + "=" * 40 + "\n")

    print("--- Testing Reservation ---")
    run_agent("I would like to reserve book ID 101 under the name Alice Vance.")
