"""myuplink api"""
import json
from typing import Callable, Dict, Optional, Tuple, Union, Any, List
from oauthlib.oauth2 import TokenExpiredError
from requests import Response
from requests_oauthlib import OAuth2Session

from myuplink.const import OAUTH_AUTHORIZE, OAUTH_TOKEN

from .error import SERVER_ERROR, CLIENT_ERROR, ServerException, ClientException
from .models import EnvironmentConfig, System, DeviceInfo, DevicePoint, SmartHomeZones, AidMode, SmartHomeCategories
from .models import Notifications, Subscriptions, SmartHomeMode, DeviceUpdate
from decimal import Decimal

class MyUplinkApi:
    def __init__(
        self,
        env: EnvironmentConfig,
        redirect_uri: Optional[str] = None,
        scope: Optional[str] = None,
        token: Optional[Dict[str, str]] = None,
        token_updater: Optional[Callable[[str], None]] = None,
    ):

        self.client_id = env.client_id
        self.client_secret = env.client_secret
        self.token_updater = token_updater
        self.base_url = env.base_url
        credentials = {"client_id": self.client_id, "client_secret": self.client_secret}

        self._oauth = OAuth2Session(
            client_id=self.client_id,
            token=token,
            redirect_uri=redirect_uri,
            scope=scope,
            auto_refresh_kwargs=credentials,
            token_updater=token_updater,
        )

    def get_authorization_url(self, base_url, state: Optional[str] = None) -> Tuple[str, str]:
        return self._oauth.authorization_url(base_url + OAUTH_AUTHORIZE, state)

    def request_token(
        self, base_url, authorization_response: Optional[str] = None, code: Optional[str] = None
    ) -> Dict[str, str]:
        """Fetching myUplink access and refresh tokens."""
        return self._oauth.fetch_token(
            base_url + OAUTH_TOKEN,
            authorization_response=authorization_response,
            code=code,
            client_secret=self.client_secret,
        )

    def refresh_tokens(self, base_url) -> Dict[str, Union[str, int]]:
        """Renew myUplink tokens."""
        token = self._oauth.refresh_token(base_url + OAUTH_TOKEN)
        if self.token_updater is not None:
            self.token_updater(token)
        return token

    # AidMode section
    def get_aidmode(self, device_id) -> AidMode:
        """Get aid mode state."""
        response = self.send_request("get", "/v2/devices/{0}/aidMode".format(device_id))
        return AidMode(**json.loads(response.text))

    # DeviceInfo section
    def get_device_info(self, device_id) -> DeviceInfo:
        """Device querying endpoint."""
        response = self.send_request("get", "/v2/devices/{0}".format(device_id))
        if response.text == '':
            print(str(device_id) + "returned no device info!")            
            return
            
        return DeviceInfo(**json.loads(response.text))

    def get_smart_home_categories(self, device_id) -> Response:
        """Gets the availability of smart home categories in a device."""
        response = self.send_request(
            "get", "/v2/devices/{0}/smart-home-categories".format(device_id)
        )
        return SmartHomeCategories(**json.loads(response.text.replace("-", "_")))

    def get_smart_home_zones(
        self, device_id, accept_language="en-US"
    ) -> List[SmartHomeZones]:
        """Gets the available smart home zones for a device."""
        headers = {"Accept-Language": accept_language, "Accept": "text/plain"}
        response = self.send_request(
            "get", "/v2/devices/{0}/smart-home-zones".format(device_id), headers=headers
        )
        data = []
        for u in json.loads(response.text):
            data.append(SmartHomeZones(**u))
        return data

    # DevicePoints section
    def get_device_points(self, device_id, accept_language="en-US", params=None):
        """Retrives all parameters for device"""
        headers = {"Accept-Language": accept_language, "Accept": "text/plain"}
        if params:
            response = self.send_request(
                "get",
                "/v2/devices/{0}/points?parameters={1}".format(device_id, params.replace(" ", "")),
                headers=headers,
            )
            data = []
            for u in json.loads(response.text):
                data.append(DevicePoint(**u))
            return data
        response = self.send_request(
            "get", "/v2/devices/{0}/points".format(device_id), headers=headers
        )
        data = (DevicePoint(**u) for u in json.loads(response.text))
        return data

    def patch_device(self, device_id, settings: Dict[str, str]) -> Response:
        """Change settings on device."""
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        response = self.send_request(
            "patch",
            "/v2/devices/{0}/points".format(device_id),
            headers=headers,
            data=settings,
        )
        # TODO: "Debug must be mapping not str" error
        return [DeviceUpdate(**s) for s in json.loads(response.text)]

    def patch_device_zones(self, device_id, zone_id, settings: Dict[str, str]) -> Response:
        """Updates zone settings."""
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        response = self.send_request(
            "patch",
            "/v2/devices/{0}/zones/{1}".format(device_id, zone_id),
            headers=headers,
            data=settings,
        )
        return json.loads(response.text)

    # Notification section
    def get_active_systems_notifications(
        self, system_id, page=1, itemsPerPage=10, accept_language="en-US"
    ) -> Response:
        """Retrieve active alarms for specified system."""
        headers = {"Accept-Language": accept_language, "Accept": "text/plain"}
        response = self.send_request(
            "get",
            "/v2/systems/{0}/notifications/active?page={1}&itemsPerPage={2}".format(
                system_id, page, itemsPerPage
            ),
            headers=headers,
        )
        return [Notifications(**s) for s in json.loads(response.text)["notifications"]]

    def get_all_systems_notifications(
        self, system_id, page=1, itemsPerPage=10, accept_language="en-US"
    ) -> Response:
        """Retrieve all (active, inactive and archived) alarms for specified system."""
        headers = {"Accept-Language": accept_language, "Accept": "text/plain"}
        response = self.send_request(
            "get",
            "/v2/systems/{0}/notifications?page={1}&itemsPerPage={2}".format(
                system_id, page, itemsPerPage
            ),
            headers=headers,
        )
        return [Notifications(**s) for s in json.loads(response.text)["notifications"]]

    # Premium section
    def get_premium_subscriptions(self, system_id) -> Response:
        """Finds out whether the specified system has any active premium subscriptions."""
        response = self.send_request("get", "/v2/systems/{0}/subscriptions".format(system_id))
        return [Subscriptions(**s) for s in json.loads(response.text)["subscriptions"]]

    # Systems section
    def get_systems(self, page=1, itemsPerPage=10) -> List[System]:
        "Retrives all systems associated with the authenticated account"
        response = self.send_request(
            "get", "/v2/systems/me?page={0}&itemsPerPage={1}".format(page, itemsPerPage)
        )

        return [System(**s) for s in json.loads(response.text)["systems"]]

    def put_system_smart_home_mode(self, system_id, data={"smartHomeMode": "Default"}) -> Response:
        headers = {"Accept": "*/*", "Content-Type": "application/json-patch+json"}
        response = self.send_request(
            "put", "/v2/systems/{0}/smart-home-mode".format(system_id), data=data, headers=headers
        )
        return response

    def get_system_smart_home_mode(self, system_id) -> Response:
        """Get current smart home mode of a system."""
        response = self.send_request("get", "/v2/systems/{0}/smart-home-mode".format(system_id))
        return SmartHomeMode(**json.loads(response.text))

    # Error and request
    def response_error_check(self, response: Response) -> None:
        """Test response for error and error source."""
        if response.status_code == 200:
            return
        elif response.status_code == 401:
            print("Failed Authorization!")
            print("Delete the file 'token.json' and re-authenticate for this environment.")            

        raw_content = response.text
        if "fault" in raw_content:
            error_code = response.json()["fault"]["detail"]["errorcode"]
            raise SERVER_ERROR.get(error_code, ServerException)(response.json())
        if "message" in raw_content:
            message = response.json()["message"]
            raise CLIENT_ERROR.get(message, ClientException)(response.json())
        response.raise_for_status()

    def send_request(self, method: str, path: str, **kwargs: Any) -> Response:
        """Make any request."""
        url = f"{self.base_url}{path}"
        try:
            response = getattr(self._oauth, method)(url, **kwargs)
            #print(response.request.url)
            #print(response.content)
        except TokenExpiredError:
            self._oauth.token = self.refresh_tokens()
            response = getattr(self._oauth, method)(url, **kwargs)

        self.response_error_check(response)
        return response

def CreateApi(
        self,
        env: EnvironmentConfig,
        redirect_uri: Optional[str] = None,
        scope: Optional[str] = None,
        token: Optional[Dict[str, str]] = None,
        token_updater: Optional[Callable[[str], None]] = None,
        ):
    return MyUplinkApi(
            self,
            env,
            redirect_uri,
            scope,
            token,
            token_updater
        ) 

"""
    # This has currently no use.
    def load_device_data(self, path) -> None:
        # get device's and system's data at startup or refresh
        if not pathlib.Path.exists(path):
            pathlib.Path.mkdir(path)
"""
