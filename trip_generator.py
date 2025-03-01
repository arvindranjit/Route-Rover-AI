from google import genai
from typing import Dict
import json
from models import TripRequest, TripPlan
client = genai.Client()

def generate_trip(trip_request: TripRequest) -> Dict:
    prompt = f"""
        You are an expert travel planner. Create a detailed {trip_request.duration}-day travel itinerary for {trip_request.destination} 
        with a total budget of ${trip_request.budget} for {trip_request.no_of_travelers} traveler(s). 

        ### Traveler Preferences:
        - Interests: {', '.join(trip_request.preferences.interests)}
        - Accomodation Preferences: {', '.join(trip_request.preferences.accomodation_preferences)}
        - Places to Include: {', '.join(trip_request.preferences.places_to_include)}
        - Places to Exclude: {', '.join(trip_request.preferences.places_to_exclude)}

        ### **Itinerary Requirements**:
        For each day of the trip, provide the following structured details:

        1. **Stay Information** (if applicable for that day):
        - Name of the hotel or accommodation
        - Address
        - Check-in and check-out dates
        - Cost per night

        2. **Planned Activities** (at least 2 per day):
        - Name of the activity
        - Brief but informative description
        - Specific location (including latitude and longitude)
        - Estimated cost per person
        - Duration of the activity

        3. **Total Daily Cost**:
        - Sum of accommodation, activity costs, and other necessary expenses.

        ### **Response Format**:
        Respond **only** in valid JSON format with the following structure:

        ```json
        {{
            "days": [
                {{
                    "day": 1,
                    "stay": {{
                        "name": "Hotel XYZ",
                        "address": "123 Street, City",
                        "check_in": "2025-03-01",
                        "check_out": "2025-03-02",
                        "cost": 120.0
                    }},
                    "activities": [
                        {{
                            "name": "Visit Museum",
                            "description": "Explore the city's famous museum with a guided tour.",
                            "location": {{
                                "lat": 40.7128,
                                "lon": -74.0060
                            }},
                            "estimated_cost": 25.0,
                            "duration": "3 hours"
                        }},
                        {{
                            "name": "Sunset Cruise",
                            "description": "Enjoy a relaxing cruise along the river, with live music and dinner.",
                            "location": {{
                                "lat": 40.7128,
                                "lon": -74.0060
                            }},
                            "estimated_cost": 50.0,
                            "duration": "2 hours"
                        }}
                    ],
                    "total_cost": 195.0
                }}
            ]
        }}
    """
    try:
        response = client.models.generate_content( 
        model='gemini-1.5-pro', 
        contents=prompt, 
        config={ 
            'response_mime_type': 'application/json',
            'response_schema': TripPlan, 
        })
        return response.parsed  
        
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to generate valid itinerary: {str(e)}")

