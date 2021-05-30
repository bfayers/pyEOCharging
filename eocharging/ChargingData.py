from eocharging.Helpers import eo_base_url as base_url
import requests


class Session:
    """Class that defines what a Session is"""
    def __init__(self, access_token=None, cpid=None, start_date=None, end_date=None):
        if access_token is None:
            raise Exception("No access_token provided")
        if cpid is None:
            raise Exception("No cpid provided")
        if start_date is None:
            raise Exception("No start_date provided")
        if end_date is None:
            raise Exception("No end_date provided")

        self.cpid = cpid
        self.start_date = start_date
        self.end_date = end_date

        # Fetch data from API
        url = base_url + "api/session/detail"
        payload = {
            "id": self.cpid,
            "startDate": self.start_date,
            "endDate": self.end_date,
        }
        headers = {"Authorization": "Bearer " + access_token}

        response = requests.post(url, data=payload, headers=headers)
        if response.status_code != 200:
            raise Exception("Response was not OK")

        data = response.json()

        # Calculate kWh used and cost
        self.session_kwh = 0
        self.session_cost = 0
        for point in data:
            kwh = ((point["CT2"] / 1000) * 230) / 1000 / 60
            self.session_kwh += kwh
            self.session_cost += kwh * point["Cost"]

class LiveSession:
    def __init__(self, access_token=None):
        if access_token is None:
            raise Exception("No access_token provided")
        
        url = base_url + "api/session"
        headers = {"Authorization": "Bearer " + access_token}

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception("Response was not OK")
        
        #I don't know the structure of this data until I next charge a car; so this is TODO
        data = response.json()
    
    def pause(self):
        """Used for pausing a session
        Similar to disabling/locking but also not"""
        url = base_url + "api/session/pause"
        payload = {"id": self.device_address}
        response = requests.post(url, data=payload, headers=self.headers)
        if response.status_code != 200:
            raise Exception("Response was not OK")

    def unpause(self):
        """Used for unpausing a paused session
        Similar to enabling/unlocking but also not"""
        url = base_url + "api/session/unpause"
        payload = {"id": self.device_address}
        response = requests.post(url, data=payload, headers=self.headers)
        if response.status_code != 200:
            raise Exception("Response was not OK")