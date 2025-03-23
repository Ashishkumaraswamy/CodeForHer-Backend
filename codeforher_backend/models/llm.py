from pydantic import BaseModel
from typing import List

class RouteStep(BaseModel):
    instructions: str
    distance: str
    duration: str

class RouteSafetyRequest(BaseModel):
    route_steps: List[RouteStep]

class RouteSafetyResponse(BaseModel):
    general_insights: str | dict
    safety_tips: str | dict 
    road_conditions: str | dict
    areas_of_concern: str | dict


    