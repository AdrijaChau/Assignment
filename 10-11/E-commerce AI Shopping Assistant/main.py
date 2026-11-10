import asyncio

from agent_framework.orchestrations import SequentialBuilder

from agents import (

    inventory_agent,

    pricing_agent,

    recommendation_agent

)

# ==========================================

# TASK 5: SEQUENTIAL ORCHESTRATION

# ==========================================

workflow = SequentialBuilder(

    participants=[

        inventory_agent,

        pricing_agent,

        recommendation_agent

    ],

    output_from="all"

).build()


# ==========================================

# RUN THE MULTI-AGENT WORKFLOW

# ==========================================

async def run_shopping_assistant():
    print("\n========================================")

    print("     E-COMMERCE AI SHOPPING ASSISTANT")

    print("========================================")

    print("\nModel: GPT-OSS-20B")

    print("Provider: Groq")

    print("\nThree agents are ready!")

    print("1. Inventory Agent")

    print("2. Pricing Agent")

    print("3. Recommendation Agent")

    print("\nType 'exit' to stop the application.")

    while True:

        user_request = input("\nCustomer: ").strip()

        if user_request.lower() in ["exit", "quit"]:
            print("\nThank you for using the shopping assistant!")

            break

        if not user_request:
            print("Please enter a valid request.")

            continue

        print("\nProcessing your request...")

        try:

            result = await workflow.run(user_request)

            outputs = result.get_outputs()

            if not outputs:
                print("No response received from the agents.")

                continue

            print("\n========================================")

            print("          AGENT RESULTS")

            print("========================================")

            for output in outputs:

                for message in output.messages:

                    if message.role == "assistant":
                        agent_name = message.author_name or "AI Agent"

                        print(f"\n--- {agent_name} ---")

                        print(message.text)

            print("\n========================================")

            print("          REQUEST COMPLETED")

            print("========================================")

        except  Exception as e:
   print("\nError while processing request:")
   print("Error type:", type(e).__name__)
   print("Error details:", repr(e))
   cause = e.__cause__
   while cause:
       print("\nUnderlying error:")
       print(repr(cause))
       if hasattr(cause, "response"):
           try:
               print("API response:", cause.response.text)
           except Exception:
               pass
       cause = cause.__cause__


# ==========================================

# APPLICATION ENTRY POINT

# ==========================================

if __name__ == "__main__":
    asyncio.run(run_shopping_assistant())
