from __future__ import annotations

import itertools
import os.path
import re
from collections import defaultdict
from functools import lru_cache
from typing import (
    Any,
    ClassVar,
    Dict,
    Mapping,
    Sequence,
    Tuple,
    Union,
    Optional,
    cast,
    overload,
)

import pint
import pint.converters
import pint.errors
import pint.util
from numpy import ndarray
from typing_extensions import TypeGuard

from .dtr_map import DTR_MAP
from .types import (
    DTRCode,
    MeasurementObject,
    PintUnitId,
    Point as Point,
    PointObject,
    PolygonObject,
    UnitId,
    UnitsFormat,
    number,
)

__all__ = [
    "convert",
    "get_conversion_factor",
    "display_conversion_factors",
    "UnitConverter",
]

_units = pint.UnitRegistry(autoconvert_offset_to_baseunit=True)
_units.load_definitions(
    os.path.join(os.path.dirname(__file__), "custom_unit_definitions.pintdef")
)
_units.default_system = "syngenta"

TEMPERATURE_UNITS = frozenset({"C", "F", "K"})


@lru_cache(maxsize=None)
def get_conversion_factor(
    unit_from: UnitId, unit_to: UnitId, precision: int = 6
) -> float:
    if unit_from in TEMPERATURE_UNITS or unit_to in TEMPERATURE_UNITS:
        raise ValueError("temperature units aren't multiplicative")
    q = cast(pint.Quantity, _units.Quantity(1.0, internal_to_pint(unit_from)))
    q.ito(internal_to_pint(unit_to))
    return round(q.magnitude, precision)


DEFAULT_PRECISION = 6


@overload
def convert(
    value: Union[number, str],
    unit_from: UnitId,
    unit_to: UnitId,
    precision: int = DEFAULT_PRECISION,
) -> float:
    ...


@overload
def convert(
    value: ndarray,
    unit_from: UnitId,
    unit_to: UnitId,
    precision: int = DEFAULT_PRECISION,
) -> ndarray:
    ...


def convert(
    value: Union[number, str, ndarray],
    unit_from: UnitId,
    unit_to: UnitId,
    precision: int = DEFAULT_PRECISION,
) -> Union[float, ndarray]:
    """
    Converts a value from one unit to a compatible one.

    Args:
        value (Union[int, float, str, ndarray]): The value(s) to convert.
        unit_from (UnitId): The internal unit name that the value is currently in.
        unit_to (UnitId): The internal unit name that the value should be converted to.
        precision (int): Number of decimal places to round the factor to - helps prevent floating point errors.

    Returns:
        Union[float, ndarray]: The converted value(s). If the input is an int, float, or string,
            the resulting value is a float. If the input is a numpy array, the resulting value
            is a numpy array.
    """
    try:
        factor = get_conversion_factor(unit_from, unit_to, precision)
    except ValueError:
        q = cast(pint.Quantity, _units.Quantity(value, internal_to_pint(unit_from)))
        q.ito(internal_to_pint(unit_to))
        return q.magnitude
    try:
        return value * factor  # type: ignore
    except TypeError:
        return float(value) * factor


class UnitConverter:
    __instances: ClassVar[Dict[UnitsFormat, UnitConverter]] = {}
    _dtr_map: Mapping[DTRCode, UnitId]
    _format: UnitsFormat

    def __init__(self, format: UnitsFormat = "metric"):
        pass

    def __new__(cls, format: UnitsFormat = "metric"):
        self = cls.__instances.get(format)
        if self is None:
            self = super().__new__(cls)
            self._dtr_map = DTR_MAP[format]
            self._format = format
            cls.__instances[format] = self
        return self

    # avail outer convert method if users want conversion directly, but attach
    # to class here in case users want to implement childclass inheritance + overrides.
    # These lines just forward to the function, so modifications to the outer
    # scope function don't change behaviour for instance methods that use self.convert
    @overload
    def convert(
        self, value: Union[number, str], unit_from: UnitId, unit_to: UnitId
    ) -> float:
        ...

    @overload
    def convert(self, value: ndarray, unit_from: UnitId, unit_to: UnitId) -> ndarray:
        ...

    def convert(
        self,
        value: Union[number, str, ndarray],
        unit_from: UnitId,
        unit_to: UnitId,
        precision: int = DEFAULT_PRECISION,
    ) -> Union[float, ndarray]:
        """Calls `pyadapt.unitconv.convert(value, unit_from, unit_to, precision)`.

        Args:
            value (Union[int, float, str, ndarray]): The value(s) to convert.
            unit_from (UnitId): The internal unit name that the value is currently in.
            unit_to (UnitId): The internal unit name that the value should be converted to.
            precision (int): Number of decimal places to round the factor to - helps prevent floating point errors.

        Returns:
            Union[float, ndarray]: The converted value(s). If the input is an int, float, or string,
                the resulting value is a float. If the input is a numpy array, the resulting value
                is a numpy array.
        """
        return convert(value, unit_from, unit_to, precision)

    @overload
    def convert_by_dtr_code(
        self, value: Union[number, str], unit_from: UnitId, dtr_code: DTRCode
    ) -> Tuple[float, UnitId]:
        ...

    @overload
    def convert_by_dtr_code(
        self, value: ndarray, unit_from: UnitId, dtr_code: DTRCode
    ) -> Tuple[ndarray, UnitId]:
        ...

    def convert_by_dtr_code(
        self, value: Union[number, str, ndarray], unit_from: UnitId, dtr_code: DTRCode
    ) -> Tuple[Union[float, ndarray], UnitId]:
        unit_to = self._dtr_map[dtr_code]
        return self.convert(value, unit_from, unit_to), unit_to

    def convert_summary(self, data: Any):
        """
        Canonizes all measurement objects found nested within `data`.
        Only lists and dicts within `data` are searched recursively.
        All measurement objects are expected to have a string `value` key.

        Args:
            data (Union[Dict, List]): An arbitrary nested data structure,
                ideally containing only dicts and lists and measurement objects.
        """
        if _is_measurement_object(data):
            self.__convert_measurement_object(data)
        elif isinstance(data, list):
            for item in data:
                self.convert_summary(item)
        elif isinstance(data, dict):
            for item in data.values():
                self.convert_summary(item)

    def __convert_measurement_object(self, measurement_object: MeasurementObject):
        try:
            converted_value, converted_value_unit = self.convert_by_dtr_code(
                float(measurement_object["value"]),
                unit_from=measurement_object["uom"],
                dtr_code=measurement_object["dtr_code"],
            )
        except KeyError:  # specific dtr code doesn't exist, mainly for backwards compatibility
            pass
        else:
            measurement_object["value"] = str(converted_value)
            measurement_object["uom"] = converted_value_unit

    #
    # Vestigial methods, kept for backwards compability
    #

    @staticmethod
    def get_centroid(
        vertexes: Sequence[Sequence[number]],
    ) -> Tuple[Union[int, float], Union[int, float]]:
        len_vertexes = len(vertexes)
        x_sum = 0
        y_sum = 0
        for x_vtx, y_vtx, *_ in vertexes:
            x_sum += x_vtx
            y_sum += y_vtx
        x = x_sum / len_vertexes
        y = y_sum / len_vertexes
        return x, y

    @staticmethod
    def polygon_to_point(geom: PolygonObject) -> PointObject:
        if geom["coordinates"][0][0] == geom["coordinates"][0][-1]:
            geom["coordinates"][0].pop()

        point = UnitConverter.get_centroid(geom["coordinates"][0])

        return {
            "type": "Point",
            "coordinates": point,
        }  # tuples are JSON-serializable, even named ones


@lru_cache(maxsize=None)
def internal_to_pint(unit: UnitId) -> PintUnitId:
    unit = re.sub(r"(-?[0-9]+)", R"**\1", unit)
    unit = re.sub(r"^\[", "(", unit, count=1)
    unit = unit.replace("[", "*(").replace("]", ")")
    return unit


def display_conversion_factors(
    target_units: Optional[Sequence[str]] = None,
) -> Dict[str, Dict[str, number]]:
    """
    Convenience function to show the conversion factors used internally.

    Args:
        target_units: optional list of units to display conversion factors for

    Returns:
        2-layered dictionary in format of:

        {
            unit_from: {
                unit_to_a: <factor>,
                unit_to_b: <factor>
                ...
            }
        ...
        }

    """
    from pprint import pprint

    units = target_units or [unit for unit in dir(_units) if not unit.startswith("_")]

    conversions = defaultdict(dict)
    for unit_from, unit_to in itertools.product(units, units):
        try:
            factor = get_conversion_factor(unit_from=unit_from, unit_to=unit_to)
        except Exception:
            pass
        else:
            conversions[unit_from].update({unit_to: factor})

    conversions = dict(conversions)

    pprint(conversions)

    return conversions


def _is_measurement_object(object: Any) -> TypeGuard[MeasurementObject]:
    try:
        return {
            "uom",
            "value",
            "dtr_code",
        } <= object.keys()  # is {"uom", "value", "dtr_code"} a subset of object.keys()
    except AttributeError:
        return False
