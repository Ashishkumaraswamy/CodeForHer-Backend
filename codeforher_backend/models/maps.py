from typing import Optional

from pydantic import BaseModel, Field

from codeforher_backend.enum_store.enums import RankByCategory
from codeforher_backend.models.common import Location


class RouteRequest(BaseModel):
    origin: Location
    destination: Location

class NearbySafeSpotsRequest(BaseModel):
    current_location: Location
    place_types: Optional[list[str]] = None
    radius: Optional[int] = None
    rank_by: Optional[RankByCategory] = Field(RankByCategory.DISTANCE, description="Rank by category")