from pydantic import BaseModel
from typing import List, Dict

class Location(BaseModel):
    lat: float
    lon: float

class Preferences(BaseModel):
    interests: List[str]
    accomodation_preferences: List[str]
    places_to_include: List[str]
    places_to_exclude: List[str]

class TripRequest(BaseModel):
    destination: str
    budget: float
    duration: int
    no_of_travelers: int
    preferences: Preferences

class Activity(BaseModel):
    name: str
    description: str
    location: Location
    estimated_cost: float
    duration: str

class Stay(BaseModel):
    name: str
    address: str
    location: Location
    check_in: str
    check_out: str
    cost: float

class DayPlan(BaseModel):
    day: int
    stay: Stay
    activities: List[Activity]
    total_cost: float

class TripPlan(BaseModel):
    days: List[DayPlan]