import requests
from station_info import StationInfo


class StationInfoParser:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StationInfoParser, cls).__new__(cls)
            cls._instance._stations = {}

        return cls._instance

    def _fetch_all(self):
        data = requests.get(
            "https://gbfs.urbansharing.com/rowermevo.pl/station_information.json",
            headers={
                "Client-Identifier": "imalyi-mevo(https://github.com/imalyi/mevo)"
            },
        ).json()
        self._last_updated = int(data["last_updated"])
        return data["data"]["stations"]

    def _parse_stations(self):
        for raw_station in self._fetch_all():
            station_id = int(raw_station.get("station_id"))
            lat = float(raw_station.get("lat"))
            lon = float(raw_station.get("lon"))
            address = str(raw_station.get("address"))
            name = str(raw_station.get("name"))
            self._stations[station_id] = StationInfo(
                lat=lat, lon=lon, address=address, name=name
            )

    def __getitem__(self, station_id: int) -> StationInfo:
        if not self._stations:
            self._parse_stations()

        return self._stations.get(station_id)
