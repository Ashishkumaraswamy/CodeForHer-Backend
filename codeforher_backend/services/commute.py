from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from typing import Dict, Optional, Union

from codeforher_backend.enum_store.enums import TripStatus
from codeforher_backend.models.config import ServiceConfig
from codeforher_backend.models.trips import Trip, TripRequest
from codeforher_backend.utils.helpers import raise_service_exception


class TripsService:
    def __init__(self, service_config: ServiceConfig):
        """Initialize MongoDB connection"""
        self.mongo_config = service_config.mongo_config
        self.jwt_config = service_config.jwt_config
        self.client = MongoClient(service_config.mongo_config.get_mongo_uri())
        self.db = self.client[self.mongo_config.database]
        self.trip = self.db["trips"]

    def close_connection(self):
        """Closes the MongoDB connection"""
        self.client.close()

    def add_trip(self, trip: TripRequest) -> Dict:
        """Registers a new user"""

        trip_json = trip.model_dump()
        trip_json["user_id"] = ObjectId(trip.user_id)

        result = self.trip.insert_one(trip_json)
        return {
            "message": "Trip Added successfully",
            "trip_id": str(result.inserted_id),
        }

    def end_trip(self, trip_id: str) -> Dict:
        """Ends a trip"""
        trip = self.trip.find_one({"_id": ObjectId(trip_id)})
        if not trip:
            raise_service_exception(400, "Trip Id provided does not exists")
        self.trip.update_one(
            {"_id": ObjectId(trip_id)}, {"$set": {"status": TripStatus.COMPLETED, "updated_at": datetime.now()}}
        )
        return {
            "message": "Trip ended successfully",
            "trip_id": trip_id,
        }

    def cancel_trip(self, trip_id: str) -> Dict:
        """Ends a trip"""
        trip = self.trip.find_one({"_id": ObjectId(trip_id)})
        if not trip:
            raise_service_exception(400, "Trip Id provided does not exists")
        self.trip.update_one(
            {"_id": ObjectId(trip_id)}, {"$set": {"status": TripStatus.CANCELLED, "updated_at": datetime.now()}}
        )
        return {
            "message": "Trip cancelled successfully",
            "trip_id": trip_id,
        }

    def get_trip(self, trip_id: Optional[str] = None, user_id: Optional[str] = None) -> Optional[
        Union[Dict, list[Dict]]]:
        """Retrieves a trip by ID, by user ID, or all trips"""

        query = {}

        if trip_id:
            try:
                query["_id"] = ObjectId(trip_id)
            except Exception as e:
                raise_service_exception(400, f"Invalid Trip ID format: {e}")

        if user_id:
            query["user_id"] = ObjectId(user_id)

        # Fetch trips based on the query
        trips = list(self.trip.find(query))

        if not trips:
            return None

        # Convert ObjectId to string for all trips
        for trip in trips:
            trip["_id"] = str(trip["_id"])
            trip["user_id"] = str(trip["user_id"])

        # Return single trip as a dict if filtering by `trip_id`
        if trip_id and len(trips) == 1:
            return trips[0]

        return trips

    def update_trip(self, trip_id: str, update_data: dict) -> Dict:
        """Updates a trip with the given data"""
        # Validate the trip ID
        trip_object_id = ""

        try:
            trip_object_id = ObjectId(trip_id)
        except Exception as e:
            raise_service_exception(400, f"Invalid Trip ID format: {e}")

        # Check if the trip exists
        existing_trip = self.trip.find_one({"_id": trip_object_id})
        if not existing_trip:
            raise_service_exception(404, "Trip ID does not exist")

        # Add an updated_at timestamp to the update data
        update_data["updated_at"] = datetime.now()

        # Update the trip
        result = self.trip.update_one(
            {"_id": trip_object_id},
            {"$set": update_data}
        )

        # Check if the update was successful
        if result.matched_count == 0:
            raise_service_exception(400, "No trip was updated")

        return {
            "message": "Trip updated successfully",
            "trip_id": trip_id,
            "modified_count": result.modified_count
        }

    def delete_trip(self, trip_id: str) -> Dict:
        """Deletes a trip by ID"""

        trip_object_id = ""

        # Validate the trip ID format
        try:
            trip_object_id = ObjectId(trip_id)
        except Exception as e:
            raise_service_exception(400, f"Invalid Trip ID format: {e}")

        # Check if the trip exists
        existing_trip = self.trip.find_one({"_id": trip_object_id})
        if not existing_trip:
            raise_service_exception(404, "Trip ID does not exist")

        # Delete the trip
        result = self.trip.delete_one({"_id": trip_object_id})

        # Verify if the trip was deleted
        if result.deleted_count == 0:
            raise_service_exception(400, "Failed to delete the trip")

        return {
            "message": "Trip deleted successfully",
            "trip_id": trip_id
        }
