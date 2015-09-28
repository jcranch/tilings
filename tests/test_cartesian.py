from unittest import TestCase

from tiling2_polygon import regular_polygon
from tiling4_prod22 import cartesian_product

from general import TilingTest


class CartesianProductTest(TestCase, TilingTest):

    def setUp(self):
        self.t = cartesian_product(regular_polygon(5), regular_polygon(6))

    def test_type(self):
        self.type_tiling4(self.t)

    def test_numerics(self):
        self.assertEqual(len(self.t.vertices), 5*6)
        self.assertEqual(len(self.t.edges), 5*6 + 5*6)
        self.assertEqual(len(self.t.faces), 1*6 + 5*6 + 5*1)
        self.assertEqual(len(self.t.volumes), 1*6 + 5*1)
        self.assertEqual(len(self.t.hypervolumes), 1*1)
