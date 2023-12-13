import xmltodict
import requests as rq
from datetime import datetime, timedelta
from metar_taf_parser.parser.parser import MetarParser

BASE_URL = "https://tgftp.nws.noaa.gov/data/observations/metar/stations/"
BASE_URL_TAF = "https://www.aviationweather.gov/adds/dataserver_current/httpparam"
BASE_URL_SIGMET = "https://www.aviationweather.gov/cgi-bin/json/IsigmetJSON.php"


class NWS:
    def __init__(self):
        self.session = rq.Session()

    def get_last_metar(self, id):
        url = BASE_URL + id + ".TXT"
        time, raw_metar = self.session.get(url).text.split("\n", 1)
        return {
            "time": datetime.strptime(time, "%Y/%m/%d %H:%M"),
            "metar": MetarParser().parse(raw_metar),
        }

    def get_raw_taf(self, id):
        params = {
            "dataSource": "tafs",
            "requestType": "retrieve",
            "format": "xml",
            "hoursBeforeNow": 1,
            "mostRecent": "true",
            "stationString": id,
        }
        response = self.session.get(BASE_URL_TAF, params=params)
        xml_data = response.text
        raw = self._convert_xml_to_dict(xml_data)["response"]["data"]["TAF"]["raw_text"]
        return raw

    def get_last_taf(self, id):
        params = {
            "dataSource": "tafs",
            "requestType": "retrieve",
            "format": "xml",
            "hoursBeforeNow": 1,
            "mostRecent": "true",
            "stationString": id,
        }
        response = self.session.get(BASE_URL_TAF, params=params)
        xml_data = response.text
        forecasts = self._convert_xml_to_dict(xml_data)["response"]["data"]["TAF"][
            "forecast"
        ]
        return forecasts

    def get_taf_flight_time(self, id, flight_time: float):
        taf = self.get_last_taf(id)
        now_utc = datetime.utcnow()
        forecast_time = now_utc + timedelta(hours=flight_time)
        list_forecast = []

        for forecast in taf:
            init_time = datetime.strptime(
                forecast["fcst_time_from"], "%Y-%m-%dT%H:%M:%SZ"
            )
            final_time = datetime.strptime(
                forecast["fcst_time_to"], "%Y-%m-%dT%H:%M:%SZ"
            )

            if init_time < forecast_time < final_time:
                list_forecast.append(forecast)

        return list_forecast

    def get_taf_values(self, id, flight_time: float):
        forecast = {
            "vis": float,
            "roof": float,
            "qroof": None,
            "obst": None,
        }

        forecast_period = self.get_taf_flight_time(id, flight_time)

        for period in forecast_period:
            if "visibility_statute_mi" in period:
                forecast["vis"] = float(period["visibility_statute_mi"])
            if "sky_condition" in period:
                if type(period["sky_condition"]) is list:
                    forecast["roof"] = float(
                        period["sky_condition"][0]["@cloud_base_ft_agl"]
                    )
                    forecast["qroof"] = period["sky_condition"][0]["@sky_cover"]
                else:
                    forecast["roof"] = float(
                        period["sky_condition"]["@cloud_base_ft_agl"]
                    )
                    forecast["qroof"] = period["sky_condition"]["@sky_cover"]
            if "wx_string" in period:
                forecast["obst"] = period["wx_string"]

        return forecast

    def _convert_xml_to_dict(self, xml_data):
        return xmltodict.parse(xml_data)