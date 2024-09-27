import stat
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from typing import Optional
import datetime
from settings import Settings


class StationSaver:
    def __init__(self, settings: Settings) -> None:
        """
        Инициализация клиента для работы с InfluxDB.

        :param settings: Экземпляр класса Settings с конфигурацией для InfluxDB.
        """
        self.client = InfluxDBClient(
            url=settings.influx_url,
            token=settings.influx_token,
            org=settings.influx_org,
        )
        self.bucket = settings.influx_bucket
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def save_stations(self, stations: "Stations") -> None:
        for station in stations:
            point = (
                Point("stations")
                .field("station_id", station.station_id)
                .tag("station_name", station.name)
                .field("station_address", station.address)
                .field("station_lat", station.lat)
                .field("station_lon", station.lon)
                .field(
                    "bikes_count",
                    station.bikes_count if station.bikes_count is not None else 0,
                )
                .field(
                    "ebikes_count",
                    station.ebikes_count if station.ebikes_count is not None else 0,
                )
                .time(datetime.datetime.utcnow(), WritePrecision.NS)
            )

            # Запись точки данных в InfluxDB
            self.write_api.write(bucket=self.bucket, org=self.client.org, record=point)

    def close(self) -> None:
        """Закрытие подключения к InfluxDB."""
        self.client.close()
