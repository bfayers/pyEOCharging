import requests
from datetime import datetime, timedelta
import time
from requests.api import head

from requests.models import Response
from eocharging.Helpers import eo_base_url as base_url
from eocharging.ChargingData import Session, LiveSession


class Device:
    def __init__(
        self,
        device_address=None,
        access_token=None,
        hub_address=None,
        charger_model=None,
        hub_model=None,
        hub_serial=None,
    ):
        if device_address is None:
            raise Exception("No device_address provided")
        if access_token is None:
            raise Exception("No access_token provided")
        # Commented out for now as these aren't strictly necesarry
        # if hub_address is None:
        #     raise Exception("No hub_address provided")
        # if charger_model is None:
        #     raise Exception("No charger_model provided")
        # if hub_model is None:
        #     raise Exception("No hub_model provided")
        # if hub_serial is None:
        #     raise Exception("No hub_serial provided")

        self.device_address = device_address
        self.headers = {"Authorization": "Bearer " + access_token}
        self.access_token = access_token
        # Commented out for now as these aren't strictly necesarry
        # self.hub_address = hub_address
        # self.charger_model = charger_model
        # self.hub_model = hub_model
        # self.hub_serial = hub_serial

    def enable(self):
        """Used for enabling a disabled charger, also known as unlocking"""
        url = base_url + "api/mini/enable"
        payload = {"id": self.device_address}
        response = requests.post(url, data=payload, headers=self.headers)
        if response.status_code != 200:
            raise Exception("Response was not OK")

    def disable(self):
        """Used for disabling an enbaled charger, also known as locking"""
        url = base_url + "api/mini/disable"
        payload = {"id": self.device_address}
        response = requests.post(url, data=payload, headers=self.headers)
        if response.status_code != 200:
            raise Exception("Response was not OK")

    def get_sessions(self, start=None, end=None):
        """Get history of charging sessions the device has performed
        If no start or end timestamps (epoch) are provided then this will return all sessions"""
        payload = {}
        if start is not None:
            payload["startDate"] = start
        if end is not None:
            payload["endDate"] = end

        if "start" not in payload.keys():
            payload = {"startDate": 0, "endDate": int(time.time())}

        url = base_url + "api/session/history"
        response = requests.post(url, data=payload, headers=self.headers)
        if response.status_code != 200:
            raise Exception("Response was not OK")

        data = response.json()
        sessions = []
        for session in data:
            sessions.append(
                Session(
                    access_token=self.access_token,
                    cpid=session["CPID"],
                    start_date=session["PiTime"],
                    end_date=session["ESTime"],
                )
            )

        return sessions

    def get_live_session(self):
        url = base_url + "api/session/alive"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            return None
        else:
            return LiveSession(access_token=self.access_token)
