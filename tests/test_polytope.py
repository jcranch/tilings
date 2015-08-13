import unittest

from tiling4_polytope import *
from vector4 import Vector4

from general import TilingTest


class PentatopeTest(unittest.TestCase, TilingTest):

    def setUp(self):
        self.t = pentatope()

    def test_equilateral(self):
        self.assertSpherical(self.t)
        self.assertEqualEdgeLengths(self.t)

    def test_type(self):
        self.type_tiling4(self.t)

    def test_numerics(self):
        self.assertEqual(len(self.t.vertices), 5)
        self.assertEqual(len(self.t.edges), 10)
        self.assertEqual(len(self.t.faces), 10)
        self.assertEqual(len(self.t.volumes), 5)
        self.assertEqual(len(self.t.hypervolumes), 1)

    def test_regularity(self):
        l = list(self.t.vertices)
        s = set((l[i]-l[j]).norm() for i in xrange(5) for j in xrange(i+1,5))
        x = s.pop()
        for y in s:
            self.assertAlmostEqual(x,y)


class HypercubeTest(unittest.TestCase, TilingTest):

    def setUp(self):
        self.t = hypercube()

    def test_equilateral(self):
        self.assertSpherical(self.t)
        self.assertEqualEdgeLengths(self.t)

    def test_type(self):
        self.type_tiling4(self.t)

    def test_numerics(self):
        self.assertEqual(len(self.t.vertices), 16)
        self.assertEqual(len(self.t.edges), 32)
        self.assertEqual(len(self.t.faces), 24)
        self.assertEqual(len(self.t.volumes), 8)
        self.assertEqual(len(self.t.hypervolumes), 1)


class Cell16Test(unittest.TestCase, TilingTest):

    def setUp(self):
        self.t = cell16()

    def test_equilateral(self):
        self.assertSpherical(self.t)
        self.assertEqualEdgeLengths(self.t)

    def test_type(self):
        self.type_tiling4(self.t)

    def test_numerics(self):
        self.assertEqual(len(self.t.vertices), 8)
        self.assertEqual(len(self.t.edges), 24)
        self.assertEqual(len(self.t.faces), 32)
        self.assertEqual(len(self.t.volumes), 16)
        self.assertEqual(len(self.t.hypervolumes), 1)


class Cell24Test(unittest.TestCase, TilingTest):

    def setUp(self):
        self.t = cell24()

    def test_equilateral(self):
        self.assertSpherical(self.t)
        self.assertEqualEdgeLengths(self.t)

    def test_type(self):
        self.type_tiling4(self.t)

    def test_numerics(self):
        self.assertEqual(len(self.t.vertices), 24)
        self.assertEqual(len(self.t.edges), 96)
        self.assertEqual(len(self.t.faces), 96)
        self.assertEqual(len(self.t.volumes), 24)
        self.assertEqual(len(self.t.hypervolumes), 1)


class Cell120Test(unittest.TestCase, TilingTest):

    def setUp(self):
        self.t = cell120()

    def test_equilateral(self):
        self.assertSpherical(self.t)
        self.assertEqualEdgeLengths(self.t)

    def test_type(self):
        self.type_tiling4(self.t)

    def test_numerics(self):
        self.assertEqual(len(self.t.vertices), 600)
        self.assertEqual(len(self.t.edges), 1200)
        self.assertEqual(len(self.t.faces), 720)
        self.assertEqual(len(self.t.volumes), 120)
        self.assertEqual(len(self.t.hypervolumes), 1)


class Cell600Test(unittest.TestCase, TilingTest):

    def setUp(self):
        self.t = cell600()

    def test_equilateral(self):
        self.assertSpherical(self.t)
        self.assertEqualEdgeLengths(self.t)

    def test_type(self):
        self.type_tiling4(self.t)

    def test_numerics(self):
        self.assertEqual(len(self.t.vertices), 120)
        self.assertEqual(len(self.t.edges), 720)
        self.assertEqual(len(self.t.faces), 1200)
        self.assertEqual(len(self.t.volumes), 600)
        self.assertEqual(len(self.t.hypervolumes), 1)


class EquivalenceTest(unittest.TestCase):

    def setUp(self):
        self.p1 = pentatope()
        self.p2 = pentatope().translate(Vector4(4,5,6,7))
        self.c1 = hypercube()
        self.c2 = hypercube().scale(2.5)
        n = lambda x: None
        self.p1a = self.p1.map(n, n, n, n, n)
        self.p2a = self.p2.map(n, n, n, n, n)
        self.c1a = self.c1.map(n, n, n, n, n)
        self.c2a = self.c2.map(n, n, n, n, n)

    def test_isometries(self):
        self.assertEqual(len(list(self.p1.isometries(self.p2))), 1)
        self.assertEqual(len(list(self.p1.isometries(self.c1))), 0)
        self.assertEqual(len(list(self.c1.isometries(self.c2))), 0)
        self.assertEqual(len(list(self.p1a.isometries(self.p2a))), 120)
        self.assertEqual(len(list(self.p1a.isometries(self.c1a))), 0)
        self.assertEqual(len(list(self.c1a.isometries(self.c2a))), 0)

    def test_isometric(self):
        self.assertTrue(self.p1a.isometric(self.p2a))
        self.assertFalse(self.p1a.isometric(self.c1a))
        self.assertFalse(self.c1a.isometric(self.c2a))

    def test_isomorphisms(self):
        self.assertEqual(len(list(self.p1.isomorphisms(self.p2))), 1)
        self.assertEqual(len(list(self.p1.isomorphisms(self.c1))), 0)
        self.assertEqual(len(list(self.c1.isomorphisms(self.c2))), 1)
        self.assertEqual(len(list(self.p1a.isomorphisms(self.p2a))), 120)
        self.assertEqual(len(list(self.p1a.isomorphisms(self.c1a))), 0)

    def test_isomorphic(self):
        self.assertTrue(self.p1a.isomorphic(self.p2a))
        self.assertFalse(self.p1a.isomorphic(self.c1a))
        self.assertTrue(self.c1a.isomorphic(self.c2a))
