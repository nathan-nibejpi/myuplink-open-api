<p align=center>
    <img src="https://myuplink.com/myUplink_logo.png"/>
</p>


### A python library that supports the myUplink Open API

Documentation:  [here](https://dev.myuplink.com/login
)

## Get developer credentials

1. Create a free myUplink account  [here](https://myuplink.com/login)
2. Login in dev site [here](https://dev.myuplink.com/login
)
3. Create a client in https://dev.myuplink.com/apps
4. The API supports two authorizasion flows. Read the documentation.
5. For authorizasion code flow to work the Redirect URL must hava a value.
4. If aiming for Authorizasion Code Flow Grant, pls observe the refresh token is on time use only.
5. Use the credentials in the example(s) below.
6. Good luck.


## Installation

```
pip install myuplink-open-api
```

## Example usage

Login, retrive system(s) and device(s). This example requests data for the first device of the first system and print updated values 

```python
import pathlib
import json
from urllib.parse import urlparse, parse_qs
import dictdiffer
from time import sleep
from datetime import datetime

# project code modules.
from lib.myuplink_api import MyUplinkApi

# Credentials & authorizasion constants
client_id = r"<CLIENT_ID>"
client_secret = r"<CLIENT_SECRET>"
redir_url = "<CALLBACK_URL>"
scope = r"READSYSTEM WRITESYSTEM offline_access" # Do not change 
state = r"x" # Can be a variable. See OAuth documentation.

# Example of storing the token (string) in working directory.
token_dir_path = pathlib.Path.joinpath(pathlib.Path.cwd(), "token")
token_full_path = pathlib.Path.joinpath(token_dir_path, "token.json")


def get_token():
    try:
        if pathlib.Path.exists(token_full_path):
            with open(token_full_path, "r") as read_file:
                return json.load(read_file)
    except IOError:
        pass


def set_token(token) -> None:
    if not pathlib.Path.exists(token_dir_path):
        pathlib.Path.mkdir(token_dir_path)
    with open(token_full_path, "w") as outfile:
        json.dump(token, outfile)


api = MyUplinkApi(
    client_id,
    client_secret,
    redir_url,
    scope,
    token_updater=set_token,
    token=get_token(),
)

# Eternal loop to request values every 15 seconds
while True:

    if not pathlib.Path.exists(token_full_path):
        authorization_url, _ = api.get_authorization_url(state)
        print("Please go to {} and authorize access.".format(authorization_url))
        authorization_response = input("Enter the full callback URL: ")
        code = parse_qs(urlparse(authorization_response).query)["code"][0]
        print("You entered code: {}".format(code))
        set_token(api.request_token(code=code))

    # Get systems/me at startup and print to terminal.
    if not "my_systems" in locals():
        my_systems = api.get_systems(1, 100)
        first_system_first_device = my_systems[0].devices[0]["id"]

    # Get Device data
    device_points = api.get_device_points(first_system_first_device)

    # Print changes only
    if not "old_device_points" in locals():
        old_device_points = []

    # Only updated values during loop.
    for diff in list(dictdiffer.diff(device_points, old_device_points)):
        print(diff)
        old_device_points = device_points

    # Print timestamp and wait 15 seconds
    now = datetime.now()
    print(now.strftime("%m/%d/%Y, %H:%M:%S"))
    sleep(15)
```
