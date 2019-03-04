import unittest

from vector2 import Vector2
from equivdict import EquivDict
from tiling2_polygon import regular_polygon


class EquivDictTest(unittest.TestCase):

    def test_polygon_dict(self):

        """
        Tests the capacity of an EquivDict to store polygons up to
        isometry.
        """

        d = EquivDict(invariant = lambda x: x.invariant(),
                      equiv = lambda x,y:x.isometric(y))

        p1 = regular_polygon(5, centre=Vector2(1,2), theta=0.1)
        p2 = regular_polygon(5, centre=Vector2(3,4), theta=0.2)
        p3 = regular_polygon(6, centre=Vector2(5,6), theta=0.3)
        p4 = regular_polygon(6, centre=Vector2(7,8), theta=0.4, radius=2.5)
        p5 = regular_polygon(7, centre=Vector2(9,10), theta=0.5)

        self.assertEqual(len(d), 0)

        d[p1] = "A"
        self.assertEqual(d[p1], "A")
        self.assertEqual(d[p2], "A")
        self.assertEqual(len(d), 1)

        d[p2] = "B"
        self.assertEqual(d[p1], "B")
        self.assertEqual(d[p2], "B")
        self.assertEqual(len(d), 1)

        d[p3] = "C"
        self.assertEqual(d[p1], "B")
        self.assertEqual(d[p2], "B")
        self.assertEqual(d[p3], "C")
        self.assertEqual(len(d), 2)

        d[p4] = "D"
        self.assertEqual(d[p1], "B")
        self.assertEqual(d[p2], "B")
        self.assertEqual(d[p3], "C")
        self.assertEqual(d[p4], "D")
        self.assertEqual(len(d), 3)

        d[p5] = "E"
        self.assertEqual(d[p1], "B")
        self.assertEqual(d[p2], "B")
        self.assertEqual(d[p3], "C")
        self.assertEqual(d[p4], "D")
        self.assertEqual(d[p5], "E")
        self.assertEqual(len(d), 4)
