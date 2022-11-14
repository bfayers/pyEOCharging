import time
from datetime import datetime, timedelta

import requests
from requests.api import head
from requests.models import Response

from eocharging.ChargingData import LiveSession, Session
from eocharging.Helpers import eo_base_url as base_url


class chargeOpts:
    def __init__(self,cpid=None, scheduleWDay=None,scheduleWEnd=None,tariffWDay=None,tariffWEnd=None,appSchedWDay=None,appSchedWEnd=None,solarMin=None,timeMode=None,solarMode=None,opMode=None,pricePeak=None,priceOffPeak=None,tnid=None,tariffZone=None):
        if cpid is None:
            raise Exception("No cpid provided")
        if scheduleWDay is None and\
           scheduleWEnd is None and\
           tariffWDay is None and\
           tariffWEnd is None and\
           appSchedWDay is None and\
           appSchedWEnd is None and\
           solarMin is None and\
           timeMode is None and\
           solarMode is None and\
           opMode is None and\
           pricePeak is None and\
           priceOffPeak is None and\
           tnid is None and\
           tariffZone is None:
           raise Exception("Must provide at least one of scheduleWDay, scheduleWEnd, tariffWDay, tariffWEnd, appSchedWDay, appSchedWEnd, solarMin, timeMode, solarMode, opMode, pricePeak, priceOffPeak, tnid, or tariffZone")
                
        self.cpid = cpid
        self.scheduleWDay = scheduleWDay
        self.scheduleWEnd = scheduleWEnd
        self.tariffWDay = tariffWDay
        self.tariffWEnd = tariffWEnd
        self.appSchedWDay = appSchedWDay
        self.appSchedWEnd = appSchedWEnd
        self.solarMin = solarMin
        self.timeMode = timeMode
        self.solarMode = solarMode
        self.opMode = opMode
        self.pricePeak = pricePeak
        self.priceOffPeak = priceOffPeak
        self.tnid = tnid
        self.tariffZone = tariffZone



class Device:
    def __init__(
        self,
        device_address=None,
        access_token=None,
        is_disabled=None,
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
        self.hub_serial = hub_serial
        self.is_disabled = is_disabled
        # Commented out for now as these aren't strictly necesarry
        # self.hub_address = hub_address
        # self.charger_model = charger_model
        # self.hub_model = hub_model

    def get_chargeOpts(self):
        """Retrieves full list of charger options - these can also be set using set_chargeOpts"""
        url = base_url + "api/user"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception("Response was not OK")
        else:
            data = response.json()
            data = data['chargeOpts']
            chargeOpt = chargeOpts(
                cpid=data['cpid'],
                scheduleWDay=data['scheduleWDay'],
                scheduleWEnd=data['scheduleWEnd'],
                tariffWDay=data['tariffWDay'],
                tariffWEnd=data['tariffWEnd'],
                appSchedWDay=data['appSchedWDay'],
                appSchedWEnd=data['appSchedWEnd'],
                solarMin=data['solarMin'],
                timeMode=data['timeMode'],
                solarMode=data['solarMode'],
                opMode=data['opMode'],
                pricePeak=data['pricePeak'],
                priceOffPeak=data['priceOffPeak'],
                tnid=data['tnid'],
                tariffZone=data['tariffZone']
            )
            return chargeOpt

    def set_chargeOpts(self, opts: chargeOpts=None):

        if opts is None:
            raise Exception("Must provide options to set")

        url = base_url + "api/user/updateChargeOpts"

        payload = {}
        payload["cpid"] = opts.cpid
        if opts.scheduleWDay is not None:
            payload["scheduleWDay"] = opts.scheduleWDay
        if opts.scheduleWEnd is not None:
            payload['scheduleWEnd'] = opts.scheduleWEnd
        if opts.tariffWDay is not None:
            payload['tariffWDay'] = opts.tariffWDay
        if opts.tariffWEnd is not None:
            payload['tariffWEnd'] = opts.tariffWEnd
        if opts.appSchedWDay is not None:
            payload['appSchedWDay'] = opts.appSchedWDay
        if opts.appSchedWEnd is not None:
            payload['appSchedWEnd'] = opts.appSchedWEnd
        if opts.solarMin is not None:
            payload['solarMin'] = opts.solarMin
        if opts.timeMode is not None:
            payload['timeMode'] = opts.timeMode
        if opts.solarMode is not None:
            payload['solarMode'] = opts.solarMode
        if opts.opMode is not None:
            payload['opMode'] = opts.opMode
        if opts.pricePeak is not None:
            payload['pricePeak'] = opts.pricePeak
        if opts.priceOffPeak is not None:
            payload['priceOffPeak'] = opts.priceOffPeak
        if opts.tnid is not None:
            payload['tnid'] = opts.tnid
        if opts.tariffZone is not None:
            payload['tariffZone'] = opts.tariffZone           

        response = requests.post(url, headers=self.headers, data=payload)
        if response.status_code != 200:
            raise Exception("Response was not OK")
        else:
            return self.get_chargeOpts()


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
