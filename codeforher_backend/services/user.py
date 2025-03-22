from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
from typing import Dict, Optional
import bcrypt
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

# Environment variables
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "safety_app")
JWT_SECRET = os.getenv("JWT_SECRET", "my_secret_key")
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_MINUTES = 30
JWT_REFRESH_EXPIRY_DAYS = 7


class UserService:
    def __init__(self):
        """Initialize MongoDB connection"""
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.users = self.db["users"]

    def close_connection(self):
        """Closes the MongoDB connection"""
        self.client.close()

    # 🚀 SIGN UP
    def signup(self, user_data: Dict) -> Dict:
        """Registers a new user"""
        # Check if user already exists
        if self.users.find_one({"email": user_data["email"]}):
            return {"error": "User already exists"}

        # Hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(user_data["password"].encode("utf-8"), salt)

        user_data["password"] = hashed_password
        user_data["created_at"] = datetime.utcnow()
        user_data["updated_at"] = datetime.utcnow()

        result = self.users.insert_one(user_data)
        return {
            "message": "User created successfully",
            "user_id": str(result.inserted_id)
        }

    # 🔑 LOGIN
    def login(self, email: str, password: str) -> Dict:
        """Authenticates user and generates access & refresh tokens"""
        user = self.users.find_one({"email": email})
        if not user:
            return {"error": "User not found"}

        # Verify password
        if not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
            return {"error": "Invalid password"}

        # Generate tokens
        access_token = self.generate_token(user["_id"], expires_in=JWT_EXPIRY_MINUTES)
        refresh_token = self.generate_token(user["_id"], expires_in=JWT_REFRESH_EXPIRY_DAYS * 24 * 60)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    # 🔁 REFRESH TOKEN
    def refresh_token(self, token: str) -> Dict:
        """Generates a new access token using a refresh token"""
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            user_id = payload["user_id"]

            # Generate new access token
            new_access_token = self.generate_token(user_id, expires_in=JWT_EXPIRY_MINUTES)

            return {
                "access_token": new_access_token
            }
        except jwt.ExpiredSignatureError:
            return {"error": "Refresh token expired"}
        except jwt.InvalidTokenError:
            return {"error": "Invalid token"}

    # 🔍 GET USER BY ID
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Retrieves a user by ID"""
        user = self.users.find_one({"_id": ObjectId(user_id)}, {"password": 0})
        if user:
            user["_id"] = str(user["_id"])
            return user
        return None

    # 🛠️ UPDATE USER
    def update_user(self, user_id: str, update_data: Dict) -> Dict:
        """Updates user details"""
        update_data["updated_at"] = datetime.utcnow()

        result = self.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            return {"error": "User not found"}

        return {"message": "User updated successfully"}

    # 🛠️ DELETE USER (Optional)
    def delete_user(self, user_id: str) -> Dict:
        """Deletes a user (soft deletion with `deleted_at`)"""
        result = self.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"deleted_at": datetime.utcnow()}}
        )

        if result.matched_count == 0:
            return {"error": "User not found"}

        return {"message": "User deleted successfully"}

    # 🔒 TOKEN GENERATION
    def generate_token(self, user_id: str, expires_in: int) -> str:
        """Generates JWT token"""
        payload = {
            "user_id": str(user_id),
            "exp": datetime.utcnow() + timedelta(minutes=expires_in)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token
