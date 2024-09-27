from station_info_parser import StationInfoParser
import datetime


class Station:
    def __init__(
        self,
        *,
        station_id: int,
        ebikes_count: int,
        bikes_count: int,
        time: datetime.datetime,
    ) -> None:
        self.station_id = station_id
        self.ebikes_count = ebikes_count
        self.bikes_count = bikes_count
        self.time = time

    def __repr__(self) -> str:
        return f"Station(station_id={self.station_id}, ebikes_count={self.ebikes_count=}, bikes_count={self.bikes_count=}, time={self.time})"

    def __str__(self) -> str:
        return (
            f"Station(station_id={self.station_id}, name={self.name}, "
            f"address={self.address}, ebikes_count={self.ebikes_count}, bikes_count={self.bikes_count}, time={self.time})"
        )

    @property
    def name(self) -> str:
        return StationInfoParser()[self.station_id].name

    @property
    def address(self) -> str:
        return StationInfoParser()[self.station_id].address

    @property
    def lat(self) -> float:
        return StationInfoParser()[self.station_id].lat

    @property
    def lon(self) -> float:
        return StationInfoParser()[self.station_id].lon

    def __eq__(self, value: object, /) -> bool:
        return (
            value.address == self.address
            and value.name == self.name
            and value.lat == self.lat
            and value.lon == self.lon
        )

    def __hash__(self) -> int:
        return hash(", ".join([self.address, self.name, str(self.lat), str(self.lon)]))
