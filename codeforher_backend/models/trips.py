from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from codeforher_backend.enum_store.enums import TripStatus
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

class TripRequest(BaseModel):
    user_id: str  # Reference to the user
    start_location: Location  # Start point details
    end_location: Location  # End point details
    route: Optional[List[RoutePoint]]=None  # List of route points
    distance: Optional[int] = None  # Distance as string (e.g., "120 km")
    duration: Optional[int] = None  # Duration as string (e.g., "2 hours")
    status: TripStatus = Field(TripStatus.ONGOING, description="Status of the trip")  # Valid statuses
    detour_alerts: Optional[List[DetourAlert]] = []  # List of detour alerts
    anomaly_alerts: Optional[List[AnomalyAlert]] = []  # List of anomaly alerts
    created_at: Optional[datetime] = Field(datetime.now(), description="Timestamp of the trip creation")
    updated_at: Optional[datetime] = Field(datetime.now(), description="Timestamp of the trip update")

class Trip(TripRequest):
    id: str = Field(..., alias="_id")  # MongoDB ObjectId as string

