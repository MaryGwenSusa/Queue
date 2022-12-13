from typing import NamedTuple

class City(NamedTuple): #extend a named tuple to ensure that your node objects are hashable, which is required by networkx; could also use a properly configured data class
    name: str
    country: str
    year: int | None
    latitude: float
    longitude: float
