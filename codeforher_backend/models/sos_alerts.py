from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from datetime import datetime

from codeforher_backend.enum_store.enums import SOSAlertMessageStatus
from codeforher_backend.models.common import Location, EmergencyContact


class EmergencyContactAlert(EmergencyContact):
    alert_status: SOSAlertMessageStatus = Field(
        ..., description="Status of the Alert Messages sent"
    )
    alert_time: Optional[datetime]=Field(datetime.now(), description="Time the Alert was sent")


class SOSMessage(BaseModel):
    id: str = Field(..., alias="_id")  # MongoDB ObjectId as string

class SOSMessageRequest(BaseModel):
    user_id: str  # Reference to the user
    trip_id: Optional[str] = None  # Reference to the trip
    location: Location  # Embedded location details
    emergency_contacts_alerted: Optional[List[EmergencyContactAlert]] = None
    message: str
    voice_clip: Optional[HttpUrl] = None  # Optional voice recording URL
    created_at: Optional[datetime] = Field(datetime.now(), description="Time the SOS Message was created at")
    updated_at: Optional[datetime] = Field(datetime.now(), description="Time the SOS Message was updated at")