
import json

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

from app.tools.langchain_tools import (
    lookup_trip_tool,
    weather_tool
)

llm = ChatOllama(
    model="qwen2.5:7b",
    temperature=0.3
)


def generate_advisory(
    user_query: str,
    employee_id: str,
    session_id: str,
    trip_id: str = None
):

    system_prompt = """
    You are an intelligent Travel Advisory Assistant.

    Your responsibilities:
    1. Help employees plan business trips.
    2. Provide destination and weather information.
    3. Suggest suitable travel recommendations.
    4. Consider employee travel policies.
    5. Give clear and practical responses.

    Use the provided trip and weather information.
    Never invent trip details or weather conditions.
    Clearly mention when information is unavailable.
    """

    retrieved_data = {}

    # Step 1: Retrieve trip information
    if trip_id:
        trip_data = lookup_trip_tool.invoke({
            "trip_id": trip_id
        })

        retrieved_data["trip"] = json.loads(trip_data)

        # Step 2: Retrieve weather information
        trip = retrieved_data["trip"]

        if "destination" in trip:
            weather_data = weather_tool.invoke({
                "destination": trip["destination"],
                "start_date": trip["start_date"],
                "end_date": trip["end_date"]
            })

            retrieved_data["weather"] = json.loads(weather_data)

    # Step 3: Prepare context for LLM
    context = json.dumps(retrieved_data, indent=2)

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(
            content=f"""
            Employee ID: {employee_id}

            User Query: {user_query}

            Retrieved Trip and Weather Information:
            {context}

            Generate a travel advisory using the available information.
            """
        )
    ]

    # Step 4: Generate advisory
    response = llm.invoke(messages)

    return response.content


