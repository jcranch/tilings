import unittest

from vector3 import Vector3
from tiling3_polyhedron import *

from general import TilingTest


class TetrahedronTest(unittest.TestCase, TilingTest):

    def setUp(self):
        self.t = tetrahedron()

    def test_equilateral(self):
        self.assertSpherical(self.t)
        self.assertEqualEdgeLengths(self.t)

    def test_type(self):
        self.type_tiling3(self.t)

    def test_numerics(self):
        self.assertEqual(len(self.t.vertices), 4)
        self.assertEqual(len(self.t.edges), 6)
        self.assertEqual(len(self.t.faces), 4)
        self.assertEqual(len(self.t.volumes), 1)


class CubeTest(unittest.TestCase, TilingTest):

    def setUp(self):
        self.t = cube()

    def test_equilateral(self):
        self.assertSpherical(self.t)
        self.assertEqualEdgeLengths(self.t)

    def test_type(self):
        self.type_tiling3(self.t)

    def test_numerics(self):
        self.assertEqual(len(self.t.vertices), 8)
        self.assertEqual(len(self.t.edges), 12)
        self.assertEqual(len(self.t.faces), 6)
        self.assertEqual(len(self.t.volumes), 1)


class OctahedronTest(unittest.TestCase, TilingTest):

    def setUp(self):
        self.t = octahedron()

    def test_equilateral(self):
        self.assertSpherical(self.t)
        self.assertEqualEdgeLengths(self.t)

    def test_type(self):
        self.type_tiling3(self.t)

    def test_numerics(self):
        self.assertEqual(len(self.t.vertices), 6)
        self.assertEqual(len(self.t.edges), 12)
        self.assertEqual(len(self.t.faces), 8)
        self.assertEqual(len(self.t.volumes), 1)


class DodecahedronTest(unittest.TestCase, TilingTest):

    def setUp(self):
        self.t = dodecahedron()

    def test_equilateral(self):
        self.assertSpherical(self.t)
        self.assertEqualEdgeLengths(self.t)

    def test_type(self):
        self.type_tiling3(self.t)

    def test_numerics(self):
        self.assertEqual(len(self.t.vertices), 20)
        self.assertEqual(len(self.t.edges), 30)
        self.assertEqual(len(self.t.faces), 12)
        self.assertEqual(len(self.t.volumes), 1)


class IcosahedronTest(unittest.TestCase, TilingTest):

    def setUp(self):
        self.t = icosahedron()

    def test_equilateral(self):
        self.assertSpherical(self.t)
        self.assertEqualEdgeLengths(self.t)

    def test_type(self):
        self.type_tiling3(self.t)

    def test_numerics(self):
        self.assertEqual(len(self.t.vertices), 12)
        self.assertEqual(len(self.t.edges), 30)
        self.assertEqual(len(self.t.faces), 20)
        self.assertEqual(len(self.t.volumes), 1)


class EquivalenceTest(unittest.TestCase):

    def setUp(self):
        self.c1 = cube()
        self.c2 = cube().translate(Vector3(4,5,6))
        self.o1 = octahedron()
        self.o2 = octahedron().scale(2.5)
        self.c1a = self.c1.map(lambda x:None, lambda x:None,
                               lambda x:None, lambda x:None)
        self.c2a = self.c2.map(lambda x:None, lambda x:None,
                               lambda x:None, lambda x:None)
        self.o1a = self.o1.map(lambda x:None, lambda x:None,
                               lambda x:None, lambda x:None)
        self.o2a = self.o2.map(lambda x:None, lambda x:None,
                               lambda x:None, lambda x:None)

    def test_isometries(self):
        self.assertEqual(len(list(self.c1.isometries(self.c2))), 1)
        self.assertEqual(len(list(self.c1.isometries(self.o1))), 0)
        self.assertEqual(len(list(self.o1.isometries(self.o2))), 0)
        self.assertEqual(len(list(self.c1a.isometries(self.c2a))), 48)
        self.assertEqual(len(list(self.c1a.isometries(self.o1a))), 0)
        self.assertEqual(len(list(self.o1a.isometries(self.o2a))), 0)

    def test_isometric(self):
        self.assertTrue(self.c1a.isometric(self.c2a))
        self.assertFalse(self.c1a.isometric(self.o1a))
        self.assertFalse(self.o1a.isometric(self.o2a))

    def test_isomorphisms(self):
        self.assertEqual(len(list(self.c1.isomorphisms(self.c2))), 1)
        self.assertEqual(len(list(self.c1.isomorphisms(self.o1))), 0)
        self.assertEqual(len(list(self.o1.isomorphisms(self.o2))), 1)
        self.assertEqual(len(list(self.c1a.isomorphisms(self.c2a))), 48)
        self.assertEqual(len(list(self.c1a.isomorphisms(self.o1a))), 0)
        self.assertEqual(len(list(self.o1a.isomorphisms(self.o2a))), 48)

    def test_isomorphic(self):
        self.assertTrue(self.c1a.isomorphic(self.c2a))
        self.assertFalse(self.c1a.isomorphic(self.o1a))
        self.assertTrue(self.o1a.isomorphic(self.o2a))
