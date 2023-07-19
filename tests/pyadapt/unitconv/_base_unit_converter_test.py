import functools
from unittest import TestCase, SkipTest
from abc import ABCMeta, abstractmethod
import numpy as np
from pyadapt.unitconv import UnitConverter, number


class BaseUnitConverterTestCase(TestCase, metaclass=ABCMeta):
    @classmethod
    def setUpClass(cls):
        """Prevent unittest from attempting to run this as a standalone test case."""
        if cls is BaseUnitConverterTestCase:
            raise SkipTest("Skip BaseTest tests, it's a base class")
        super().setUpClass()

    @functools.cached_property
    def converter(self) -> UnitConverter:
        return self.get_converter()

    @abstractmethod
    def get_converter(self) -> UnitConverter:
        ...

    def _test_skeleton(self, factor: number, unit_from: str, unit_to: str):
        convert = functools.partial(
            self.converter.convert, unit_from=unit_from, unit_to=unit_to
        )

        self.assertEqual(factor, convert(1))
        np.testing.assert_array_equal(
            np.array([factor, factor]), convert(np.array([1, 1]))
        )
