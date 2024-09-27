import requests
import datetime
from station import Station


class Stations:
    def __init__(self, refresh_frequency: int = 200) -> None:
        self._stations = set()
        self._refresh_frequency = refresh_frequency

    def _fetch_all(self) -> list[dict]:
        data = requests.get(
            "https://gbfs.urbansharing.com/rowermevo.pl/station_status.json",
            headers={
                "Client-Identifier": "imalyi-mevo(https://github.com/imalyi/mevo)"
            },
        ).json()
        self._last_updated = data["last_updated"]
        return data["data"]["stations"]

    @property
    def _is_refresh_required(self):
        return (
            datetime.datetime.now().timestamp() - self._last_updated
            > self._refresh_frequency
        )

    def _parse_stations(self) -> None:
        self._stations.clear()
        for raw_station in self._fetch_all():
            bikes_count = None
            ebikes_count = None

            for bike in raw_station.get("vehicle_types_available", []):
                if bike.get("vehicle_type_id") == "bike":
                    bikes_count = int(bike.get("count"))
                if bike.get("vehicle_type_id") == "ebike":
                    ebikes_count = int(bike.get("count"))
            station_id = int(raw_station.get("station_id"))
            self._stations.add(
                Station(
                    station_id=station_id,
                    ebikes_count=ebikes_count,
                    bikes_count=bikes_count,
                    time=datetime.datetime.fromtimestamp(self._last_updated),
                )
            )

    def __iter__(self):
        if not self._stations or self._is_refresh_required:
            self._parse_stations()
        return self.StationsIterator(self)

    class StationsIterator:
        def __init__(self, outer) -> None:
            self.outer = outer
            self.iterator = iter(self.outer._stations)

        def __next__(self) -> Station:
            return next(self.iterator)
