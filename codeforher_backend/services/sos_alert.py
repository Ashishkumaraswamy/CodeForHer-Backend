from datetime import datetime

from pymongo import MongoClient
from bson import ObjectId
from typing import Dict, Optional, Union

from starlette import status

from codeforher_backend.enum_store.enums import SOSAlertMessageStatus
from codeforher_backend.models.config import ServiceConfig
from codeforher_backend.models.sos_alerts import SOSMessageRequest, EmergencyContactAlert
from codeforher_backend.services.user import UserService

from twilio.rest import Client

from codeforher_backend.utils.helpers import raise_service_exception


class SOSMessageService:
    def __init__(self, service_config: ServiceConfig):
        """Initialize MongoDB connection"""
        self.mongo_config = service_config.mongo_config
        self.jwt_config = service_config.jwt_config
        self.client = MongoClient(service_config.mongo_config.get_mongo_uri())
        self.db = self.client[self.mongo_config.database]
        self.sos = self.db["sos_alerts"]
        self.user_service = UserService(service_config)
        self.twilio_config = service_config.twilio_config
        self.twilio_client = Client(service_config.twilio_config.account_sid, service_config.twilio_config.auth_token)

    def close_connection(self):
        """Closes the MongoDB connection"""
        self.client.close()

    def send_alert(self, alert_request: SOSMessageRequest, contact_name: Optional[str] = None) -> Dict:

        if contact_name is None:
            emergency_contacts = self.user_service.get_emergency_contacts(alert_request.user_id)
        else:
            emergency_contacts = self.user_service.get_contact_details(alert_request.user_id, contact_name)
            if emergency_contacts is None:
                raise_service_exception(status.HTTP_404_NOT_FOUND, "Contact not found")
            emergency_contacts = [emergency_contacts]

        alert_message = f"""
        {alert_request.message}

        This is my location:

        Latitude: {alert_request.location.latitude}
        Longitude: {alert_request.location.longitude}
        Address: {alert_request.location.address}
        """
        emergency_alert_status = []
        for contact in emergency_contacts:
            alert_status = EmergencyContactAlert(
                name=contact.name,
                phone=contact.phone,
                relationship=contact.relationship,
                alert_status=SOSAlertMessageStatus.PENDING,
            )

            try:
                self.twilio_client.messages.create(
                    body=alert_message,
                    from_=self.twilio_config.phone_number,
                    to=contact.phone
                )
                print(f"Alert sent to {contact.name} at {contact.phone}")
                alert_status.alert_status = SOSAlertMessageStatus.SENT
            except Exception:
                print(f"Failied to send alert to {contact.name} at {contact.phone}")
                alert_status.alert_status = SOSAlertMessageStatus.FAILED
            emergency_alert_status.append(alert_status)

        alert_request.emergency_contacts_alerted = emergency_alert_status
        alert_request.message = alert_message

        alert_json = alert_request.model_dump()
        alert_json["user_id"] = ObjectId(alert_request.user_id)
        if alert_json["trip_id"] is not None:
            alert_json["trip_id"] = ObjectId(alert_request.trip_id)

        result = self.sos.insert_one(alert_json)

        return {
            "message": "Alert broadcasted and inserted successfully",
            "alert_id": str(result.inserted_id),
        }

    def get_alert(self, alert_id: Optional[str] = None, trip_id: Optional[str]=None, user_id: Optional[str] = None) -> Optional[Union[dict, list[dict]]]:

        query = {}

        if alert_id:
            try:
                query["_id"] = ObjectId(trip_id)
            except Exception as e:
                raise_service_exception(400, f"Invalid Trip ID format: {e}")

        if user_id:
            query["user_id"] = ObjectId(user_id)

        if trip_id:
            query["user_id"] = ObjectId(user_id)

        # Fetch trips based on the query
        alerts = list(self.sos.find(query))

        if not alerts:
            raise_service_exception(status.HTTP_404_NOT_FOUND, "No Alerts found")

        # Convert ObjectId to string for all trips
        for alert in alerts:
            alert["_id"] = str(alert["_id"])
            alert["user_id"] = str(alert["user_id"])
            alert["trip_id"] = str(alert["trip_id"]) if alert["trip_id"] is not None else alert["trip_id"]

        # Return single trip as a dict if filtering by `trip_id`
        if alert_id and len(alerts) == 1:
            return alerts[0]

        return alerts

    def update_alert(self, alert_id: str, update_data: dict) -> Dict:
        """Updates a trip with the given data"""
        # Validate the alert ID
        alert_object_id = ""

        try:
            alert_object_id = ObjectId(alert_id)
        except Exception as e:
            raise_service_exception(400, f"Invalid Trip ID format: {e}")

        # Check if the trip exists
        existing_trip = self.sos.find_one({"_id": alert_object_id})
        if not existing_trip:
            raise_service_exception(404, "Trip ID does not exist")

        # Add an updated_at timestamp to the update data
        update_data["updated_at"] = datetime.now()

        # Update the trip
        result = self.sos.update_one(
            {"_id": alert_object_id},
            {"$set": update_data}
        )

        # Check if the update was successful
        if result.matched_count == 0:
            raise_service_exception(400, "No trip was updated")

        return {
            "message": "Alert updated successfully",
            "trip_id": alert_id,
            "modified_count": result.modified_count
        }

    def delete_trip(self, alert_id: str) -> Dict:
        """Deletes a alert by ID"""

        # Validate the alert ID
        alert_object_id = ""

        # Validate the trip ID format
        try:
            alert_object_id = ObjectId(alert_id)
        except Exception as e:
            raise_service_exception(400, f"Invalid Alert ID format: {e}")

        # Check if the trip exists
        existing_trip = self.sos.find_one({"_id": alert_object_id})
        if not existing_trip:
            raise_service_exception(404, "Trip ID does not exist")

        # Delete the trip
        result = self.sos.delete_one({"_id": alert_object_id})

        # Verify if the trip was deleted
        if result.deleted_count == 0:
            raise_service_exception(400, "Failed to delete the trip")

        return {
            "message": "Alert deleted successfully",
            "trip_id": alert_id
        }
