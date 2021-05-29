import requests
from eocharging.Device import Device
from eocharging.Helpers import eo_base_url as base_url


class Manager:
    def __init__(self, username=None, password=None):
        if username is None:
            raise Exception("No username provided")
        if password is None:
            raise Exception("No password provided")

        # Login
        payload = {"grant_type": "password", "username": username, "password": password}
        response = requests.post(base_url + "Token", data=payload)
        if response.status_code != 200:
            raise Exception("Response was not OK")
        response = response.json()

        self.headers = {"Authorization": "Bearer " + response["access_token"]}
        self.access_token = response["access_token"]

    def get_devices(self):

        url = base_url + "api/mini/list"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception("Response not OK")
        data = response.json()

        devices = []
        for device in data:
            devices.append(
                Device(device_address=device["address"], access_token=self.access_token)
            )
        return devices
