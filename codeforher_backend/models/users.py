from pydantic import BaseModel, EmailStr, Field, StringConstraints
from typing import List, Optional, Annotated
from datetime import datetime

from codeforher_backend.models.common import EmergencyContact


class Preferences(BaseModel):
    location_sharing: bool = True
    SOS_active: bool = True
    safe_radius: int = Field(100, gt=0)  # Ensure radius is positive
    voice_assist: bool = True

class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    phone: Annotated[str, StringConstraints(pattern=r"^\+91-\d{8,10}$")]
    home_address: str = Field(..., description="Home address of the user")
    password: str
    emergency_contacts: List[EmergencyContact]
    preferences: Optional[Preferences] = Field(
        Preferences(),
        description="Preferences of the features the users want to avail from the system",
    )
    created_at: datetime | str
    updated_at: datetime | str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class User(SignupRequest):
    id: Optional[str] = Field(None, alias="_id")  # MongoDB ObjectId represented as string

