from dataclasses import Field

from pydantic import BaseModel


class Location(BaseModel):
    latitude: float
    longitude: float
    address: str

class EmergencyContact(BaseModel):
    name: str
    phone: str = Field(..., regex=r"^\+91-\d{8,10}$")
    relationship: str
