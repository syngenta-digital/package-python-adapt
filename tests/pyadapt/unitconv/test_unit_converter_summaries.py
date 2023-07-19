import json
from unittest import TestCase
from pathlib import Path

from pyadapt.unitconv import UnitConverter


class TestUnitConvertSummaries(TestCase):
    def setUp(self) -> None:
        self.converter = UnitConverter(format="imperial")

        tests_dir = Path(__file__).parent.parent.parent
        with (tests_dir / "seed/summary_aggregator/harvest1.json").open("r") as file:
            self.original_harvest = json.load(file)
        with (tests_dir / "seed/summary_aggregator/planting1.json").open("r") as file:
            self.original_planting = json.load(file)

        self.maxDiff = None

    def test_convert_canonical_harvest(self):
        self.converter.convert_summary(self.original_harvest)

        self.assertListEqual(
            [
                {
                    "resource_ref": "18083cfd-90fc-58f4-8c17-b1c2c8ae8c91",
                    "resource_measures": [
                        {
                            "dtr_code": "A_AREA_ALLOCATED",
                            "value": "2.374084755379869",
                            "uom": "ac",
                            "user_uom": "m2",
                        },
                        {
                            "dtr_code": "A_TIME_ALLOCATED",
                            "value": "1.8299966666666667",
                            "uom": "sec",
                            "user_uom": "hr",
                        },
                    ],
                    "resource_type": "ASSET",
                }
            ],
            self.original_harvest["asset_uses"],
        )

        self.assertListEqual(
            [
                {
                    "is_carrier": False,
                    "is_tank_mix": False,
                    "resource_measures": [
                        {
                            "dtr_code": "A_AREA_ALLOCATED",
                            "uom": "ac",
                            "user_uom": "m2",
                            "value": "2.3740973099999985",
                        },
                        {
                            "dtr_code": "A_YLD_MOISTURE",
                            "uom": "prcnt",
                            "user_uom": "prcnt",
                            "value": "21.689451689891605",
                        },
                        {
                            "dtr_code": "A_YLD_VOL_TOTAL",
                            "uom": "bu",
                            "user_uom": "bu",
                            "value": "880.1193443784",
                        },
                        {
                            "dtr_code": "A_YLD_VOL_PER_AREA",
                            "uom": "bu1ac-1",
                            "user_uom": "bu1[m2]-1",
                            "value": "370.55554216505413",
                        },
                    ],
                    "resource_ref": "1e7e1bb2-5a8a-542b-a712-df92aaf62b96",
                    "resource_type": "PRODUCT",
                }
            ],
            self.original_harvest["product_uses"],
        )

        self.assertListEqual(
            [
                {
                    "resource_measures": [
                        {
                            "dtr_code": "A_AREA_ALLOCATED",
                            "uom": "ac",
                            "user_uom": "m2",
                            "value": "2.374084755379869",
                        },
                        {
                            "dtr_code": "A_TIME_ALLOCATED",
                            "uom": "sec",
                            "user_uom": "hr",
                            "value": "1.8299966666666667",
                        },
                    ],
                    "resource_ref": "262238d1-3eb0-5dff-bff9-73b499142102",
                    "resource_type": "FIELD",
                }
            ],
            self.original_harvest["land_uses"],
        )
        self.assertListEqual(
            [
                {
                    "dtr_code": "A_AREA_TOTAL",
                    "uom": "ac",
                    "user_uom": "m2",
                    "value": "2.374084755379869",
                },
                {
                    "dtr_code": "A_TIME_TOTAL",
                    "uom": "sec",
                    "user_uom": "hr",
                    "value": "1.8299966666666667",
                },
            ],
            self.original_harvest["task_measures"],
        )

    def test_convert_canonical_planting(self):
        self.converter.convert_summary(self.original_planting)

        self.assertListEqual(
            [
                {
                    "resource_measures": [
                        {
                            "dtr_code": "A_AREA_ALLOCATED",
                            "uom": "ac",
                            "user_uom": "ha",
                            "value": "45.151599999999995",
                        },
                        {
                            "dtr_code": "A_TIME_ALLOCATED",
                            "uom": "sec",
                            "user_uom": "sec",
                            "value": "13675.0",
                        },
                        {
                            "dtr_code": "M_ACT_SPEED",
                            "uom": "mi1hr-1",
                            "user_uom": "km1hr-1",
                            "value": "5.364009230900537",
                        },
                    ],
                    "resource_ref": "UNKNOWN",
                    "resource_type": "ASSET",
                }
            ],
            self.original_planting["asset_uses"],
        )

        self.assertListEqual(
            [
                {
                    "is_carrier": "false",
                    "is_tank_mix": "false",
                    "mix_components": [],
                    "resource_measures": [
                        {
                            "dtr_code": "A_AREA_ALLOCATED",
                            "uom": "ac",
                            "user_uom": "ha",
                            "value": "37.222899999999996",
                        },
                        {
                            "dtr_code": "A_ACT_SEED_TOTAL",
                            "uom": "seeds",
                            "user_uom": "seeds",
                            "value": "5120000.0",
                        },
                        {
                            "dtr_code": "A_ACT_SEED_PER_AREA",
                            "uom": "seeds1ac-1",
                            "user_uom": "seeds1ha-1",
                            "value": "137448.79070056198",
                        },
                    ],
                    "resource_ref": "fcdaf5f6-0c4d-5eea-be90-8b68633f61c7",
                    "resource_type": "PRODUCT",
                },
                {
                    "is_carrier": "false",
                    "is_tank_mix": "false",
                    "mix_components": [],
                    "resource_measures": [
                        {
                            "dtr_code": "A_AREA_ALLOCATED",
                            "uom": "ac",
                            "user_uom": "ha",
                            "value": "7.904",
                        },
                        {
                            "dtr_code": "A_ACT_SEED_TOTAL",
                            "uom": "seeds",
                            "user_uom": "seeds",
                            "value": "1098120.0",
                        },
                        {
                            "dtr_code": "A_ACT_SEED_PER_AREA",
                            "uom": "seeds1ac-1",
                            "user_uom": "seeds1ha-1",
                            "value": "138740.14775041302",
                        },
                    ],
                    "resource_ref": "b7f5ed0e-8bf8-5859-b9ff-4845ac8ca899",
                    "resource_type": "PRODUCT",
                },
            ],
            self.original_planting["product_uses"],
        )

        self.assertListEqual(
            [
                {
                    "resource_measures": [
                        {
                            "dtr_code": "A_AREA_ALLOCATED",
                            "uom": "ac",
                            "user_uom": "ha",
                            "value": "45.151599999999995",
                        },
                        {
                            "dtr_code": "A_TIME_ALLOCATED",
                            "uom": "sec",
                            "user_uom": "sec",
                            "value": "13675.0",
                        },
                    ],
                    "resource_ref": "d5c878f1-b25b-12d6-e68f-4acd3f3ae757",
                    "resource_type": "FIELD",
                }
            ],
            self.original_planting["land_uses"],
        )

        self.assertListEqual(
            [
                {
                    "dtr_code": "A_AREA_ALLOCATED",
                    "uom": "ac",
                    "user_uom": "ha",
                    "value": "45.151599999999995",
                },
                {
                    "dtr_code": "A_TIME_ALLOCATED",
                    "uom": "sec",
                    "user_uom": "sec",
                    "value": "13675.0",
                },
            ],
            self.original_planting["task_measures"],
        )
