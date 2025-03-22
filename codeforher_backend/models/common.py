from dataclasses import Field
from typing import Annotated

from pydantic import BaseModel, StringConstraints


class Location(BaseModel):
    latitude: float
    longitude: float
    address: str


class EmergencyContact(BaseModel):
    name: str
    phone: Annotated[str, StringConstraints(pattern=r"^\+91-\d{8,10}$")]
    relationship: str
