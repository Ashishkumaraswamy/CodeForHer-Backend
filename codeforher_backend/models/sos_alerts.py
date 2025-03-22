from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from datetime import datetime

from codeforher_backend.enum_store.enums import SOSAlertMessageStatus
from codeforher_backend.models.common import Location, EmergencyContact


class EmergencyContactAlert(EmergencyContact):
    alert_status: SOSAlertMessageStatus = Field(..., description="Status of the Alert Messages sent")
    alert_time: datetime


class SOSMessage(BaseModel):
    id: str = Field(..., alias="_id")                     # MongoDB ObjectId as string
    user_id: str                                           # Reference to the user
    trip_id: str                                           # Reference to the trip
    timestamp: datetime
    location: Location                                     # Embedded location details
    emergency_contacts_alerted: List[EmergencyContactAlert]
    voice_clip: Optional[HttpUrl] = None                   # Optional voice recording URL
    created_at: datetime
    updated_at: datetime