from requests import get
from stations import Stations
from settings import Settings
from station_saver import StationSaver
import schedule
import logging
from functools import lru_cache
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@lru_cache
def get_settings():
    return Settings()


def parse_data():
    try:
        stations = Stations()
        station_saver = StationSaver(settings=get_settings())

        logging.info("Fetching and saving stations data...")
        station_saver.save_stations(stations)
        logging.info("Data saved successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    logging.info(
        f"Scheduling data parsing every {get_settings().saving_interval} seconds."
    )
    schedule.every(get_settings().saving_interval).seconds.do(parse_data)

    while True:
        schedule.run_pending()
        time.sleep(get_settings().saving_interval // 2)
