from eocharging.Helpers import eo_base_url as base_url
import requests


class Session:
    def __init__(self, access_token=None, cpid=None, start_date=None, end_date=None):
        """Nothing yet"""
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
