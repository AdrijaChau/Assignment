
from app.services.advisory import generate_advisory

response = generate_advisory(
    user_query="Give me a travel advisory for my business trip.",
    employee_id="EMP001",
    session_id="SESSION001",
    trip_id="TRIP001"
)

print("\nAI TRAVEL ADVISORY:\n")
print(response)


