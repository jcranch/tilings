import unittest

from tiling4_polytope import *

from general import TilingTest


class PentatopeTest(unittest.TestCase, TilingTest):

    def setUp(self):
        self.t = pentatope()

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

    def test_type(self):
        self.type_tiling4(self.t)

    def test_numerics(self):
        self.assertEqual(len(self.t.vertices), 120)
        self.assertEqual(len(self.t.edges), 720)
        self.assertEqual(len(self.t.faces), 1200)
        self.assertEqual(len(self.t.volumes), 600)
        self.assertEqual(len(self.t.hypervolumes), 1)
