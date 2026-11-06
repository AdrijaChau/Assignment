import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver
from guardrails import contains_pii, clean_output

from tools import (
    search_workshops,
    list_all_workshops,
    find_cheapest_workshop,
    calculate_workshop_fee
)

# STEP 1: Load environment
load_dotenv()

# STEP 2: Create model
model = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    temperature=0
)

# STEP 3: Create agent
agent = create_agent(
    model=model,
    tools=[
        search_workshops,
        list_all_workshops,
        find_cheapest_workshop,
        calculate_workshop_fee
    ],
    system_prompt=(
        "You are a Workshop AI Assistant. You can help users list workshops, search by topic, "
        "find the cheapest workshop, and calculate fees applying coupon codes when available."
    ),
    checkpointer=InMemorySaver()
)

# STEP 4: Run application
if __name__ == "__main__":
    thread_number = 1
    previous_count = 0

    print("LangChain Workshop AI Agent")
    print("Type /new for a new conversation")
    print("Type exit to quit")

    while True:
        question = input("\nYou: ").strip()

        if question.lower() == "exit":
            break

        if question.lower() == "/new":
            thread_number += 1
            previous_count = 0
            print("New conversation started.")
            continue

        if not question:
            continue

        config = {
            "configurable": {
                "thread_id": f"workshop-{thread_number}"
            }
        }

        try:
            result = agent.invoke(
                input={
                    "messages": [
                        {"role": "user", "content": question}
                    ]
                },
                config=config
            )

            messages = result["messages"]
            new_messages = messages[previous_count:]
            previous_count = len(messages)

            for message in new_messages:
                if isinstance(message, AIMessage):
                    for call in message.tool_calls:
                        print(f"[TOOL]: {call['name']}")
                        print(f"Arguments: {call['args']}")

                if isinstance(message, ToolMessage):
                    print(f"[TOOL RESULT]: {message.content}")

            print(f"\nAgent: {clean_output(messages[-1].content)}")

        except Exception as error:
            print("Error:", error)