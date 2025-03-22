from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

class EmergencyContact(BaseModel):
    name: str
    phone: str = Field(..., regex=r"^\+91-\d{8,10}$")
    relationship: str

class Preferences(BaseModel):
    location_sharing: bool
    SOS_active: bool
    safe_radius: int = Field(..., gt=0)  # Ensure radius is positive
    voice_assist: bool

class User(BaseModel):
    id: str = Field(..., alias="_id")  # MongoDB ObjectId represented as string
    name: str
    email: EmailStr
    phone: str = Field(..., regex=r"^\+91-\d{8,10}$")
    home_address: str = Field(..., description="Home address of the user")
    password: str  # Hashed password
    emergency_contacts: List[EmergencyContact]
    preferences: Optional[Preferences] = Field(None, description="Preferences of the features the users want to avail from the system")
    created_at: datetime
    updated_at: datetime