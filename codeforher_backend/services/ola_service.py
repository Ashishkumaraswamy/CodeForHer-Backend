from starlette import status

from codeforher_backend.models.common import Location
from codeforher_backend.models.config import ServiceConfig
import requests

from codeforher_backend.models.maps import RouteRequest, NearbySafeSpotsRequest
from codeforher_backend.utils.helpers import raise_service_exception


class OLAService:
    def __init__(self, service_config: ServiceConfig):
        """Initialize OLA Config"""

        self.ola_config = service_config.ola_config
        self.headers = {
            "X-Request-Id": "CodeForHer-Backend-Map-Request",
        }
        self.OLA_API_URL = "https://api.olamaps.io"

    def http_request(self, url, method="GET", params=None, data=None, timeout=20):
        """
        Send an HTTP request to the OLA API.

        Args:
            url (str): The API endpoint.
            method (str): HTTP method (GET, POST, PUT, DELETE, etc.).
            headers (dict): Request headers.
            data (dict, str, or bytes): Data payload for POST/PUT requests.
            params (dict): Query parameters for GET requests.
            timeout (int): Timeout for the request in seconds.

        Returns:
            dict: JSON response or error message.
        """
        try:
            # Convert method to uppercase
            method = method.upper()

            # Make the request
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                data=data,
                params=params,
                timeout=timeout
            )

            # Check for HTTP errors
            response.raise_for_status()

            # Return JSON response
            return response.json()

        except requests.exceptions.RequestException as e:
            raise_service_exception(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Failed to send request to OLA API: {e}")

    def get_route(self, route_request: RouteRequest):

        # Construct the URL for the OLA API
        url = (
            f"{self.OLA_API_URL}/routing/v1/directions/basic"
            f"?origin={route_request.origin.latitude},{route_request.origin.longitude}"
            f"&destination={route_request.destination.latitude},{route_request.destination.longitude}"
            f"&api_key={self.ola_config.api_key}"
        )

        response = self.http_request(url,method="POST")

        return response

    def get_distance_and_duration(self, route_request: RouteRequest) -> dict:
        # Construct the URL for the OLA API
        url = (
            f"{self.OLA_API_URL}/routing/v1/distanceMatrix/basic"
            f"?origins={route_request.origin.latitude},{route_request.origin.longitude}"
            f"&destinations={route_request.destination.latitude},{route_request.destination.longitude}"
            f"&api_key={self.ola_config.api_key}"
        )

        response = self.http_request(url, method="GET")

        processed_response = {
            "distance": response["rows"][0]["elements"][0]["distance"],
            "duration": response["rows"][0]["elements"][0]["duration"],
            "route": response["rows"][0]["elements"][0]["polyline"],
        }

        return processed_response

    def get_nearby_safe_spots(self, safe_spot_request: NearbySafeSpotsRequest):

        safe_spots = [
            "bank",
            "bus_station",
            "atm",
            "cafe",
            "hospital",
            "pharmacy",
            "shopping_mall",
            "train_station",
            "university",
            "place_of_worship"
        ]
        radius = 5000

        if safe_spot_request.place_types is not None:
            safe_spots = safe_spot_request.place_types
        safe_spots = ','.join(safe_spots)

        if safe_spot_request.radius is not None:
            radius = safe_spot_request.radius

        # Construct the URL for the OLA API
        url = (
            f"{self.OLA_API_URL}/places/v1/nearbysearch"
            f"?location={safe_spot_request.current_location.latitude},{safe_spot_request.current_location.longitude}"
            f"&types={safe_spots}"
            f"&radius={radius}"
            f"&rankBy={safe_spot_request.rank_by.value}"
            f"&api_key={self.ola_config.api_key}"
        )

        response = self.http_request(url, method="GET")

        return response
