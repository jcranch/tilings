import unittest

from vector2 import Vector2
from tiling2_polygon import regular_polygon
from restrict21 import restrict21

from general import TilingTest



class PolygonTest(TilingTest, unittest.TestCase):

    def setUp(self):
        self.tiling = regular_polygon(7, radius=1.5, theta=0.5, centre=Vector2(3,4))

    def test_type(self):
        self.type_tiling2(self.tiling)
                        
    def test_numerics(self):
        t = self.tiling
        self.assertEqual(len(t.vertices), 7)
        self.assertEqual(len(t.edges), 7)
        self.assertEqual(len(t.faces), 1)
        


class RestrictionTest(TilingTest, unittest.TestCase):

    def setUp(self):
        self.tiling = restrict21(regular_polygon(5, theta=0.1))
    
    def test_type(self):
        self.type_tiling1(self.tiling)
