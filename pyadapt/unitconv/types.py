from typing import List, Literal, Tuple, NamedTuple, TypedDict, Union
from typing_extensions import TypeAlias

DTRCode = str
UnitId = str
PintUnitId = str
UnitsFormat = Literal["metric", "canonical", "imperial"]

# NOTE: Not all of these dimension types are supported.
DimensionType = Literal[
    "distance",
    "time",
    "temperature",
    "pressure",
    "volume",
    "mass",
    "density",
    "area",
    "seeds_per_area",
    "mass_per_area",
    "volume_per_area",
    "prcnt",
    "energy",
    "power",
    "voltage",
    "electric_current",
    "frequency",
    "substance_per_area_per_time",
    "area_per_time",
    "energy_per_area",
    "electrical_conductance",
    "electrical_conductance_per_distance",
    "pixel",
    "ears_per_area",
    "count_per_area",
    "speed",
    "seeds",
    "power_per_area",
    "angle",
    "kernels_per_mass",
    "kernels",
    "bales_per_area",
    "kernels_per_ear",
    "electrical_resistance",
    "count",
]

number: TypeAlias = Union[int, float]


class MeasurementObject(TypedDict):
    value: Union[number, str]
    uom: UnitId
    dtr_code: DTRCode


class Point(NamedTuple):
    x: number
    y: number


Coordinate: TypeAlias = List[number]  # type alias
"A list of two numbers"


class PolygonObject(TypedDict):
    type: Literal["Polygon"]
    coordinates: List[List[Coordinate]]  # a list of vertexes


class PointObject(TypedDict):
    type: Literal["Point"]
    coordinates: Union[
        Coordinate, Point, Tuple[number, number]
    ]  # a list of two numbers
