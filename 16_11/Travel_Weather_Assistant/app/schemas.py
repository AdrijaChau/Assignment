
from pydantic import BaseModel, Field, ConfigDict, model_validator
from datetime import date
from typing import Optional


class TripCreate(BaseModel):
    employee_id: str = Field(min_length=1)
    destination: str = Field(min_length=2)
    start_date: date
    end_date: date
    purpose: str = Field(min_length=2)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("End date cannot be before start date")
        return self


class TripResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    trip_id: str
    employee_id: str
    destination: str
    start_date: date
    end_date: date
    purpose: str
    status: Optional[str] = "Upcoming"


class ChatRequest(BaseModel):
    employee_id: str
    session_id: str
    question: str
