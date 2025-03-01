from fastapi import FastAPI, HTTPException
from models import TripRequest, TripResponse
from trip_generator import generate_trip

app = FastAPI(
    title="Route Rover AI",
)

@app.post("/api/generate-trip", response_model=TripResponse)
async def create_trip(trip_request: TripRequest):
    try:
        itinerary = generate_trip(trip_request)
        return itinerary
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)