class StationInfo:
    def __init__(self, *, lat: float, lon: float, address: str, name: str) -> None:
        self.lat = lat
        self.lon = lon
        self.address = address
        self.name = name

    def __repr__(self) -> str:
        return f"StationInfo(name={self.name}, address={self.address}, lon={self.lon}, lat={self.lat})"

    def __str__(self) -> str:
        return self.__repr__()
