from pyadapt.unitconv import UnitConverter
from ._base_unit_converter_test import BaseUnitConverterTestCase


class TestUnitConvertFactorsMetric(BaseUnitConverterTestCase):
    def get_converter(self) -> UnitConverter:
        return UnitConverter(format="metric")

    def test_feet(self):
        factor = 0.3048
        self._test_skeleton(factor=factor, unit_from="feet", unit_to="meters")
        self._test_skeleton(factor=factor, unit_from="feet", unit_to="m")
        self._test_skeleton(factor=factor, unit_from="ft", unit_to="m")
        self._test_skeleton(factor=factor, unit_from="ft", unit_to="meter")

    def test_gallons(self):
        self._test_skeleton(factor=3.785412, unit_from="gallon", unit_to="liters")

    def test_acres(self):
        factor = 0.404687
        self._test_skeleton(factor=factor, unit_from="acre", unit_to="hectare")
        self._test_skeleton(factor=factor, unit_from="ac", unit_to="hectare")
        self._test_skeleton(factor=factor, unit_from="acre", unit_to="ha")
        self._test_skeleton(factor=factor, unit_from="ac", unit_to="ha")

    def test_gallon_per_acre(self):
        factor = 9.353919
        self._test_skeleton(factor=factor, unit_from="gal1ac-1", unit_to="l1ha-1")
        self._test_skeleton(factor=factor, unit_from="gal1[ac]-1", unit_to="l1[ha]-1")

    def test_lbs(self):
        factor = 0.453592
        self._test_skeleton(factor=factor, unit_from="lb", unit_to="kg")
        self._test_skeleton(factor=factor, unit_from="lbs", unit_to="kg")

    def test_lbs_per_acre(self):
        factor = 1.120847
        self._test_skeleton(factor=factor, unit_from="lb1ac-1", unit_to="kg1ha-1")
        self._test_skeleton(factor=factor, unit_from="lb1[ac]-1", unit_to="kg1[ha]-1")

    def test_seeds_per_acre(self):
        factor = 2.471044
        self._test_skeleton(factor=factor, unit_from="seeds1ac-1", unit_to="seeds1ha-1")
        self._test_skeleton(
            factor=factor, unit_from="seeds1[ac]-1", unit_to="seeds1[ha]-1"
        )

    def test_seeds_per_meter(self):
        factor = 10000.0
        self._test_skeleton(
            factor=factor, unit_from="seeds1[m2]-1", unit_to="seeds1ha-1"
        )
        self._test_skeleton(
            factor=factor, unit_from="seeds1[m2]-1", unit_to="seeds1[ha]-1"
        )

    def test_bu_per_acre_to_liters_per_hectare(self):
        factor = 87.07729
        self._test_skeleton(factor=factor, unit_from="bu1ac-1", unit_to="l1[ha]-1")
        self._test_skeleton(factor=factor, unit_from="bu[ac]-1", unit_to="l1[ha]-1")

    def test_mph_to_kph(self):
        self._test_skeleton(factor=1.609344, unit_from="mi1hr-1", unit_to="km1hr-1")
