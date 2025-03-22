import os

from pydantic import Field
from pydantic import BaseModel
from dotenv import load_dotenv


class MongoConfig(BaseModel):
    host: str = Field(..., description="Host name of the mongo db server")
    user: str = Field(..., description="Username for the mongo db server")
    password: str = Field(..., description="Password for the mongo db server")
    database: str = Field(..., description="Database name for the mongo db server")

    def get_mongo_uri(self) -> str:
        return f"mongodb+srv://{self.user}:{self.password}@{self.host}"


class JWTConfig(BaseModel):
    jwt_secret: str = Field(..., description="Secret key used for JWT tokens")
    jwt_algorithm: str = Field(..., description="Algorithm used for JWT tokens")
    jwt_expiry_minutes: int = Field(
        ..., description="Expiry time of JWT tokens in minutes"
    )
    jwt_refresh_expiry_days: int = Field(
        ..., description="Expiry time of JWT refresh tokens in days"
    )


class OLAApiConfig(BaseModel):
    client_id: str = Field(..., description="Client ID for the OLA API")
    api_key: str = Field(..., description="API key for the OLA API")

class TwilioConfig(BaseModel):
    account_sid: str = Field(..., description="Account SID for the Twilio API")
    auth_token: str= Field(..., description="Auth token for the Twilio API")
    phone_number: str = Field(..., description="Phone number for the Twilio API")

class ServiceConfig(BaseModel):
    mongo_config: MongoConfig = Field(
        ..., description="Configuration for the mongo db server"
    )
    jwt_config: JWTConfig = Field(..., description="Configuration for the JWT tokens")
    ola_config: OLAApiConfig = Field(..., description="Configuration for the OLA API")
    twilio_config: TwilioConfig = Field(..., description="Configuration for the Twilio API")

    @classmethod
    def load_config(cls) -> "ServiceConfig":
        load_dotenv()
        mongo_config = MongoConfig(
            host=os.getenv("MONGO_HOST", "mongodb://localhost:27017"),
            user=os.getenv("MONGO_USER", None),
            database=os.getenv("MONGO_DBNAME", "codeforher"),
            password=os.getenv("MONGO_PASSWORD"),
        )
        jwt_config = JWTConfig(
            jwt_secret=os.getenv("JWT_SECRET", "your_secret_key"),
            jwt_algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
            jwt_refresh_expiry_days=int(os.getenv("JWT_REFRESH_EXPIRY_DAYS", 7)),
            jwt_expiry_minutes=int(os.getenv("JWT_EXPIRY_MINUTES", 30)),
        )
        ola_config = OLAApiConfig(
            client_id=os.getenv("OLA_CLIENT_ID", None),
            api_key=os.getenv("OLA_API_KEY", None),
        )
        twilio_config = TwilioConfig(
            account_sid=os.getenv("TWILIO_ACCOUNT_SID", None),
            auth_token=os.getenv("TWILIO_AUTH_TOKEN", None),
            phone_number=os.getenv("TWILIO_PHONE_NUMBER", None),
        )
        return ServiceConfig(
            mongo_config=mongo_config, jwt_config=jwt_config, ola_config=ola_config, twilio_config=twilio_config
        )
