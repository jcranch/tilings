import unittest

from tiling3_polyhedron import *

from general import TilingTest


class TetrahedronTest(unittest.TestCase, TilingTest):

    def setUp(self):
        self.t = tetrahedron()

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

    def test_type(self):
        self.type_tiling3(self.t)

    def test_numerics(self):
        self.assertEqual(len(self.t.vertices), 12)
        self.assertEqual(len(self.t.edges), 30)
        self.assertEqual(len(self.t.faces), 20)
        self.assertEqual(len(self.t.volumes), 1)
