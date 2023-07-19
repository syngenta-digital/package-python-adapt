from pyadapt.unitconv import UnitConverter
from ._base_unit_converter_test import BaseUnitConverterTestCase


class TestUnitConvertFactorsOther(BaseUnitConverterTestCase):
    def get_converter(self) -> UnitConverter:
        return UnitConverter()

    def test_gallons_per_meter_squared_to_liter_acres(self):
        self._test_skeleton(
            factor=15319.079266, unit_from="gal1[m2]-1", unit_to="l1[ac]-1"
        )

    def test_gallons_per_meter_squared_to_liter_hectare(self):
        self._test_skeleton(
            factor=37854.11784, unit_from="gal1[m2]-1", unit_to="l1[ha]-1"
        )

    def test_gallons_per_meter_squared_to_gallons_acres(self):
        self._test_skeleton(
            factor=4046.87261, unit_from="gal1[m2]-1", unit_to="gal1[ac]-1"
        )

    def test_gallons_per_meter_squared_to_gallons_hectare(self):
        factor = 10000.0
        self._test_skeleton(factor=factor, unit_from="gal1[m2]-1", unit_to="gal1[ha]-1")

    def test_kph_to_mph(self):
        self._test_skeleton(factor=0.621371, unit_from="km1hr-1", unit_to="mi1hr-1")

    def test_inch_to_m(self):
        self._test_skeleton(factor=0.0254, unit_from="inch", unit_to="m")
