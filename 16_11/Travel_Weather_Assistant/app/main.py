
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from app.services.advisory import generate_advisory

app = FastAPI(
    title="Travel Weather Advisory Assistant",
    description="AI-powered business travel and weather advisory system",
    version="1.0.0"
)


class AdvisoryRequest(BaseModel):
    user_query: str
    employee_id: str
    session_id: str
    trip_id: Optional[str] = None


@app.get("/")
def home():
    return {
        "message": "Travel Weather Advisory Assistant is running!"
    }


@app.post("/advisory")
def travel_advisory(request: AdvisoryRequest):

    response = generate_advisory(
        user_query=request.user_query,
        employee_id=request.employee_id,
        session_id=request.session_id,
        trip_id=request.trip_id
    )

    return {
        "employee_id": request.employee_id,
        "session_id": request.session_id,
        "trip_id": request.trip_id,
        "advisory": response
    }
