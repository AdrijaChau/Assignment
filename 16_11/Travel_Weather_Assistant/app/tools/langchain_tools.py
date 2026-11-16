
import json
from datetime import date

from langchain_core.tools import tool

from app.database import SessionLocal
from app.models import Trip
from app.tools.weather import get_weather


@tool
def lookup_trip_tool(trip_id: str) -> str:
    """Retrieve saved business trip details from SQLite using a trip ID."""

    db = SessionLocal()

    try:
        trip = db.query(Trip).filter(
            Trip.trip_id == trip_id
        ).first()

        if not trip:
            return json.dumps({"error": "Trip not found"})

        return json.dumps({
            "trip_id": trip.trip_id,
            "employee_id": trip.employee_id,
            "destination": trip.destination,
            "start_date": trip.start_date.isoformat(),
            "end_date": trip.end_date.isoformat(),
            "purpose": trip.purpose,
            "status": trip.status
        })

    finally:
        db.close()


@tool
def weather_tool(
    destination: str,
    start_date: str,
    end_date: str
) -> str:
    """Retrieve actual weather forecast for a destination and travel dates."""

    try:
        weather = get_weather(
            destination,
            date.fromisoformat(start_date),
            date.fromisoformat(end_date)
        )

        return json.dumps(weather)

    except ValueError:
        return json.dumps({
            "error": "Invalid date format. Use YYYY-MM-DD."
        })

    except Exception as e:
        return json.dumps({
            "error": f"Weather retrieval failed: {str(e)}"
        })
