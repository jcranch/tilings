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



class EquivalenceTest(unittest.TestCase):

    def setUp(self):
        self.p1 = regular_polygon(5, theta=0.1)
        self.p2 = regular_polygon(5, theta=0.3)
        self.h1 = regular_polygon(6, theta=0.5, radius=1.0)
        self.h2 = regular_polygon(6, theta=0.7, radius=2.0)
        n = lambda x: None
        self.p1a = self.p1.map(n, n, n)
        self.p2a = self.p2.map(n, n, n)
        self.h1a = self.h1.map(n, n, n)
        self.h2a = self.h2.map(n, n, n)

    def test_isometries(self):
        self.assertEqual(len(list(self.p1.isometries(self.p2))), 1)
        self.assertEqual(len(list(self.p1.isometries(self.h1))), 0)
        self.assertEqual(len(list(self.h1.isometries(self.h2))), 0)
        self.assertEqual(len(list(self.p1a.isometries(self.p2a))), 10)
        self.assertEqual(len(list(self.p1a.isometries(self.h1a))), 0)
        self.assertEqual(len(list(self.h1a.isometries(self.h2a))), 0)

    def test_isometric(self):
        self.assertTrue(self.p1a.isometric(self.p2a))
        self.assertFalse(self.p1a.isometric(self.h1a))
        self.assertFalse(self.h1a.isometric(self.h2a))

    def test_isomorphisms(self):
        self.assertEqual(len(list(self.p1.isomorphisms(self.p2))), 1)
        self.assertEqual(len(list(self.p1.isomorphisms(self.h1))), 0)
        self.assertEqual(len(list(self.h1.isomorphisms(self.h2))), 1)
        self.assertEqual(len(list(self.p1a.isomorphisms(self.p2a))), 10)
        self.assertEqual(len(list(self.p1a.isomorphisms(self.h1a))), 0)
        self.assertEqual(len(list(self.h1a.isomorphisms(self.h2a))), 12)

    def test_isomorphic(self):
        self.assertTrue(self.p1a.isomorphic(self.p2a))
        self.assertFalse(self.p1a.isomorphic(self.h1a))
        self.assertTrue(self.h1a.isomorphic(self.h2a))
