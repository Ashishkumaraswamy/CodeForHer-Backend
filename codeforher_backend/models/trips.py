from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from codeforher_backend.models.common import Location


class RoutePoint(BaseModel):
    lat: float
    lon: float
    timestamp: datetime

class DetourAlert(BaseModel):
    timestamp: datetime
    detour_reason: str
    location: RoutePoint

class AnomalyAlert(BaseModel):
    timestamp: datetime
    reason: str

class Trip(BaseModel):
    id: str = Field(..., alias="_id")                      # MongoDB ObjectId as string
    user_id: str                                            # Reference to the user
    start_location: Location                                # Start point details
    end_location: Location                                  # End point details
    route: List[RoutePoint]                                 # List of route points
    distance: str                                           # Distance as string (e.g., "120 km")
    duration: str                                           # Duration as string (e.g., "2 hours")
    status: str = Field(..., regex="^(ongoing|completed|canceled)$")  # Valid statuses
    detour_alerts: Optional[List[DetourAlert]] = []         # List of detour alerts
    anomaly_alerts: Optional[List[AnomalyAlert]] = []       # List of anomaly alerts
    created_at: datetime
    updated_at: datetime