from pydantic import BaseModel
from typing import List

class RouteStep(BaseModel):
    instructions: str
    distance: str
    duration: str

class RouteSafetyRequest(BaseModel):
    route_steps: List[RouteStep]

class RouteSafetyResponse(BaseModel):
    general_insights: str
    safety_tips: dict 
    road_conditions: dict
    areas_of_concern: dict


    