from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
from typing import Dict, Optional, Union
import bcrypt
import jwt
from starlette import status

from codeforher_backend.models.common import EmergencyContact
from codeforher_backend.models.config import ServiceConfig
from codeforher_backend.models.users import User, LoginRequest, SignupRequest
from codeforher_backend.utils.helpers import raise_service_exception


class UserService:
    def __init__(self, service_config: ServiceConfig):
        """Initialize MongoDB connection"""
        self.mongo_config = service_config.mongo_config
        self.jwt_config = service_config.jwt_config
        self.client = MongoClient(service_config.mongo_config.get_mongo_uri())
        self.db = self.client[self.mongo_config.database]
        self.users = self.db["users"]

    def close_connection(self):
        """Closes the MongoDB connection"""
        self.client.close()

    def add_user(self, user: SignupRequest) -> Dict:
        """Registers a new user"""
        # Check if user already exists
        if self.users.find_one({"email": user.email}):
            raise_service_exception(400, "User already exists")

        # Hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), salt)

        user.password = hashed_password
        user.created_at = datetime.now()
        user.updated_at = datetime.now()

        result = self.users.insert_one(user.model_dump())
        return {
            "message": "User created successfully",
            "user_id": str(result.inserted_id),
        }

    def authenticate(self, request: LoginRequest) -> Dict:
        """Authenticates user and generates access & refresh tokens"""
        user = self.users.find_one({"email": request.email})
        if not user:
            raise_service_exception(400, "Email Id provided does not exists! Please check you email id")

        # Verify password
        if not bcrypt.checkpw(request.password.encode("utf-8"), user["password"]):
            return {"error": "Invalid password"}

        # Generate tokens
        access_token = self.generate_token(
            user["_id"], expires_in=self.jwt_config.jwt_expiry_minutes
        )
        refresh_token = self.generate_token(
            user["_id"], expires_in=self.jwt_config.jwt_refresh_expiry_days * 24 * 60
        )

        return {"access_token": access_token, "refresh_token": refresh_token, "user_id":  str(user["_id"])}

    def refresh_token(self, token: str) -> Dict:
        """Generates a new access token using a refresh token"""
        try:

            payload = jwt.decode(
                token,
                self.jwt_config.jwt_secret,
                algorithms=[self.jwt_config.jwt_refresh_expiry_days],
            )
            user_id = payload["user_id"]

            # Generate new access token
            new_access_token = self.generate_token(
                user_id, expires_in=self.jwt_config.jwt_expiry_minutes
            )

            return {"access_token": new_access_token}
        except jwt.ExpiredSignatureError:
            return {"error": "Refresh token expired"}
        except jwt.InvalidTokenError:
            return {"error": "Invalid token"}

    def get_users(self, user_id: Optional[str] = None) -> Optional[Union[dict, list[dict]]]:
        """Retrieves a user by ID or all users"""

        if user_id:
            try:
                # Fetch user by ID, excluding the password
                user = self.users.find_one({"_id": ObjectId(user_id)}, {"password": 0})

                if user:
                    # Convert ObjectId to string
                    user["_id"] = str(user["_id"])
                    return user
                return None

            except Exception as e:
                print(f"Error fetching user by ID: {e}")
                return None

        # Fetch all users, excluding passwords
        users = list(self.users.find({}, {"password": 0}))

        # Convert ObjectId to string for all users
        for user in users:
            user["_id"] = str(user["_id"])

        return users if users else None

    def update_user(self, user_id: str, update_data: dict) -> Dict:
        """Updates user details"""
        update_data["updated_at"] = datetime.utcnow()

        result = self.users.update_one(
            {"_id": ObjectId(user_id)}, {"$set": update_data}
        )

        if result.matched_count == 0:
            return {"error": "User not found"}

        return {"message": "User updated successfully"}

    def delete_user(self, user_id: str) -> Dict:
        """Deletes a user (soft deletion with `deleted_at`)"""
        result = self.users.update_one(
            {"_id": ObjectId(user_id)}, {"$set": {"deleted_at": datetime.utcnow()}}
        )

        if result.matched_count == 0:
            return {"error": "User not found"}

        return {"message": "User deleted successfully"}

    def generate_token(self, user_id: str, expires_in: int) -> str:
        """Generates JWT token"""
        payload = {
            "user_id": str(user_id),
            "exp": datetime.utcnow() + timedelta(minutes=expires_in),
        }
        token = jwt.encode(
            payload, self.jwt_config.jwt_secret, algorithm=self.jwt_config.jwt_algorithm
        )
        return token

    def get_emergency_contacts(self, user_id: str) -> list[EmergencyContact]:
        user = self.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise_service_exception(400, "User not found")
        return [EmergencyContact(**contact) for contact in user["emergency_contacts"]]

    def get_contact_details(self, user_id: str, contact_name: str) -> EmergencyContact:
        user = self.users.find_one({"_id": ObjectId(user_id)})
        user["_id"] = str(user["_id"])
        if not user:
            raise_service_exception(400, "User not found")

        user_details = User(**user)
        for contact in user_details.emergency_contacts:
            if contact.name == contact_name:
                return contact

        raise_service_exception(status.HTTP_404_NOT_FOUND, "Contact not found")

