from pyadapt.unitconv import UnitConverter
from ._base_unit_converter_test import BaseUnitConverterTestCase


class TestUnitConvertFactorsCanonical(BaseUnitConverterTestCase):
    def get_converter(self) -> UnitConverter:
        return UnitConverter(format="canonical")

    def test_gallons_per_acres_to_liter_meters(self):
        self._test_skeleton(factor=0.000935, unit_from="gal1[ac]-1", unit_to="l1[m2]-1")

    def test_liters_per_hectare_to_liter_meters(self):
        self._test_skeleton(factor=0.0001, unit_from="l1[ha]-1", unit_to="l1[m2]-1")

    def test_m3_per_hectare_to_liter_meters(self):
        self._test_skeleton(factor=0.1, unit_from="[m3]1ha-1", unit_to="l1[m2]-1")

    def test_m3_per_m2_to_liter_meters(self):
        self._test_skeleton(factor=1000.0, unit_from="m3[m2]-1", unit_to="l1[m2]-1")

    def test_bu_per_acre_to_liters_per_m2(self):
        factor = 0.008708
        self._test_skeleton(factor=factor, unit_from="bu1ac-1", unit_to="l1[m2]-1")
        self._test_skeleton(factor=factor, unit_from="bu1[ac]-1", unit_to="l1[m2]-1")
