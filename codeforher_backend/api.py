from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
import uvicorn
from structlog import get_logger

from codeforher_backend.models.config import ServiceConfig
from codeforher_backend.models.maps import RouteRequest, NearbySafeSpotsRequest, AddressRequest
from codeforher_backend.models.sos_alerts import SOSMessageRequest
from codeforher_backend.models.trips import TripRequest
from codeforher_backend.models.users import LoginRequest, SignupRequest
from codeforher_backend.services.commute import TripsService
from codeforher_backend.services.map_service import MapService
from codeforher_backend.services.sos_alert import SOSMessageService
from codeforher_backend.services.user import UserService
from codeforher_backend.utils.helpers import verify_token

LOG = get_logger("Backend API")

app = FastAPI()

# Base URL
BASE_URL = "/api"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{BASE_URL}/login")
service_config = ServiceConfig.load_config()

# ----------- AUTH ENDPOINTS ------------

@app.post(f"{BASE_URL}/auth/signup")
def signup(signup_request: SignupRequest):
    """Signup endpoint"""
    user_service = UserService(
        service_config=service_config
    )
    response = user_service.add_user(signup_request)
    user_service.close_connection()
    return response

@app.post(f"{BASE_URL}/auth/login")
def login(request: LoginRequest):
    """Login endpoint"""
    user_service = UserService(
        service_config=service_config
    )
    response = user_service.authenticate(request)
    user_service.close_connection()
    return response


@app.post(f"{BASE_URL}/auth/refresh")
def refresh_token(token: str):
    """Refresh access token using refresh token"""
    user_service = UserService(
        service_config=service_config
    )
    response = user_service.refresh_token(token)
    user_service.close_connection()
    return response

@app.get(f"{BASE_URL}/auth/users")
def get_user(token: str = Depends(oauth2_scheme), user_id: str=None):
    """Get user by ID"""

    # token_data = verify_token(service_config.jwt_config, token)
    LOG.info("User authenticated with the token successfully")

    # if user_id and user_id!=token_data.get("user_id"):
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User does not have access to see other users")

    user_service = UserService(
        service_config=service_config
    )
    response = user_service.get_users(user_id)
    user_service.close_connection()
    return response

@app.put(f"{BASE_URL}/auth/users/{{user_id}}")
def update_user(user_id: str, request: dict, token: str = Depends(oauth2_scheme)):
    """Update user details"""

    # token_data = verify_token(service_config.jwt_config, token)
    LOG.info("User authenticated with the token successfully")

    # if user_id and user_id != token_data.get("user_id"):
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN, detail="User does not have access to see other users"
    #         )

    user_service = UserService(
        service_config=service_config
    )
    response = user_service.update_user(user_id, request)
    user_service.close_connection()
    return response

# ----------- COMMUTE ENDPOINTS ------------

@app.post(f"{BASE_URL}/commute/start-trip")
def start_trip(trip_request: TripRequest, token: str = Depends(oauth2_scheme)):
    """Start a trip"""

    # verify_token(service_config.jwt_config, token)
    LOG.info("User authenticated with the token successfully")

    trip_service = TripsService(
        service_config=service_config
    )
    response = trip_service.add_trip(trip_request)
    trip_service.close_connection()
    return response

@app.get(f"{BASE_URL}/commute/end-trip/{{trip_id}}")
def end_trip(trip_id: str, token: str = Depends(oauth2_scheme)):
    """End a trip"""

    # verify_token(service_config.jwt_config, token)
    LOG.info("User authenticated with the token successfully")

    trip_service = TripsService(
        service_config=service_config
    )
    response = trip_service.end_trip(trip_id)
    trip_service.close_connection()
    return response

@app.get(f"{BASE_URL}/commute/cancel-trip/{{trip_id}}")
def cancel_trip(trip_id: str, token: str = Depends(oauth2_scheme)):
    """Cancel a trip"""

    # verify_token(service_config.jwt_config, token)
    LOG.info("User authenticated with the token successfully")

    trip_service = TripsService(
        service_config=service_config
    )
    response = trip_service.cancel_trip(trip_id)
    trip_service.close_connection()
    return response

@app.get(f"{BASE_URL}/commute/trips")
def get_trips(trip_id: str = None, user_id: str=None, token: str = Depends(oauth2_scheme)):
    # verify_token(service_config.jwt_config, token)
    LOG.info("User authenticated with the token successfully")

    trip_service = TripsService(
        service_config=service_config
    )
    response = trip_service.get_trip(trip_id, user_id)
    trip_service.close_connection()
    return response

@app.put(f"{BASE_URL}/commute/trips/{{trip_id}}")
def get_trips(trip_id: str, request: dict, token: str = Depends(oauth2_scheme)):
    # verify_token(service_config.jwt_config, token)
    LOG.info("User authenticated with the token successfully")

    trip_service = TripsService(
        service_config=service_config
    )
    response = trip_service.update_trip(trip_id, request)
    trip_service.close_connection()
    return response

@app.delete(f"{BASE_URL}/commute/trips/{{trip_id}}")
def delete_trip(trip_id: str, token: str = Depends(oauth2_scheme)):
    # verify_token(service_config.jwt_config, token)
    LOG.info("User authenticated with the token successfully")

    trip_service = TripsService(
        service_config=service_config
    )
    response = trip_service.delete_trip(trip_id)
    trip_service.close_connection()
    return response

# ----- SOS Alerts -------

@app.post(f"{BASE_URL}/sos/send-alert")
def broadcast_alert(alert_request: SOSMessageRequest, contact: str = None, token: str = Depends(oauth2_scheme)):
    """Broadcast SOS alert to emergency contacts"""

    # verify_token(service_config.jwt_config, token)
    LOG.info("User authenticated with the token successfully")

    sos_message_service = SOSMessageService(
        service_config=service_config
    )
    response = sos_message_service.send_alert(alert_request, contact)
    sos_message_service.close_connection()
    return response

@app.get(f"{BASE_URL}/sos/alerts")
def get_alerts(alert_id: str=None, trip_id: str = None, user_id: str=None, token: str = Depends(oauth2_scheme)):
    verify_token(service_config.jwt_config, token)
    LOG.info("User authenticated with the token successfully")

    sos_message_service = SOSMessageService(
        service_config=service_config
    )
    response = sos_message_service.get_alert(alert_id, trip_id, user_id)
    sos_message_service.close_connection()
    return response

# ------- OLA SERVICE --------

@app.post(f"{BASE_URL}/maps/get-route")
def get_route(request: RouteRequest, token: str = Depends(oauth2_scheme)):
    # verify_token(service_config.jwt_config, token)
    LOG.info("User authenticated with the token successfully")

    ola_service = MapService(service_config)
    response = ola_service.get_route(request)
    return response

@app.post(f"{BASE_URL}/maps/get-time-distance")
def get_time_and_distance(request: RouteRequest, token: str = Depends(oauth2_scheme)):
    # verify_token(service_config.jwt_config, token)
    LOG.info("User authenticated with the token successfully")

    ola_service = MapService(service_config)
    response = ola_service.get_distance_and_duration(request)
    return response

@app.post(f"{BASE_URL}/maps/nearby-safe-spots")
def get_nearby_safe_spots(request: NearbySafeSpotsRequest, token: str = Depends(oauth2_scheme)):
    # verify_token(service_config.jwt_config, token)
    LOG.info("User authenticated with the token successfully")

    ola_service = MapService(service_config)
    response = ola_service.get_nearby_safe_spots(request)
    return response

@app.post(f"{BASE_URL}/maps/get-latitude-longitude")
def get_latitude_longitude(request: AddressRequest, token: str = Depends(oauth2_scheme)):
    # verify_token(service_config.jwt_config, token)
    LOG.info("User authenticated with the token successfully")

    ola_service = MapService(service_config)
    response = ola_service.get_latitude_longitude(request)
    return response


def local_server(port=8080):
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == '__main__':
    LOG.info("Service initialized")
    LOG.info("Starting API server")
    local_server()