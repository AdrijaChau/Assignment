
from sqlalchemy import Column, String, Date, Integer
from app.database import Base


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)

    trip_id = Column(String, unique=True, index=True, nullable=False)

    employee_id = Column(String, nullable=False)

    destination = Column(String, nullable=False)

    start_date = Column(Date, nullable=False)

    end_date = Column(Date, nullable=False)

    purpose = Column(String, nullable=False)

    status = Column(String, default="Upcoming")
