import unittest

from restrict32 import restrict32
from tiling3_periodic import cubic_tiling3, simple_periodic_tiling3
from tiling3_polyhedron import cube
from vector2 import Vector2
from vector3 import Vector3

from general import TilingTest



class CubicTilingTest(TilingTest, unittest.TestCase):

    def setUp(self):
        self.bbox = ((-3.5,4.5),(-2.5,4.5),(-1.5,4.5))
        self.tiling = cubic_tiling3(self.bbox).translate(Vector3(4,4,4))

    def test_type(self):
        self.type_tiling3(self.tiling)

    def test_size(self):
        t = self.tiling
        self.assertEqual(len(t.vertices), 8*7*6)
        self.assertEqual(len(t.edges), 8*7*5 + 8*6*6 + 7*7*6)
        self.assertEqual(len(t.faces), 8*6*5 + 7*7*5 + 7*6*6)
        self.assertEqual(len(t.volumes), 7*6*5)

    def test_clip_type(self):
        self.type_tiling3(self.tiling.clip(2.5,7.5,2.5,7.5,2.5,7.5))

    def test_useless_clip(self):
        t1 = self.tiling
        t2 = self.tiling.clip(0,10,0,10,0,10)
        self.assertEqual(t1.vertices, t2.vertices)
        self.assertEqual(t1.edges, t2.edges)
        self.assertEqual(t1.faces, t2.faces)
        self.assertEqual(t1.volumes, t2.volumes)

    def test_restrict_type(self):
        t = restrict32(self.tiling.translate(Vector3(0,0,-3.5)))
        self.type_tiling2(t)

    def test_restrict(self):
        t = restrict32(self.tiling.translate(Vector3(0,0,-3.5)))
        self.assertEqual(len(t.vertices), 8*7)
        self.assertEqual(len(t.edges), 8*6 + 7*7)
        self.assertEqual(len(t.faces), 7*6)

    def test_restrict_then_clip_type(self):
        t = restrict32(self.tiling.translate(Vector3(0,0,-3.5)))
        t = t.clip(1.5,8.5,1.5,8.5)
        self.type_tiling2(t)

    def test_restrict_then_useless_clip(self):
        t = restrict32(self.tiling.translate(Vector3(0,0,-3.5)))
        t = t.clip(0,10,0,10)
        self.assertEqual(len(t.vertices), 8*7)
        self.assertEqual(len(t.edges), 8*6 + 7*7)
        self.assertEqual(len(t.faces), 7*6)

    def test_simple_version(self):
        n = lambda x: None
        unitcube = cube().translate(Vector3(1,1,1)).scale(0.5)
        t = self.tiling.map(n,n,n,n)
        t1 = simple_periodic_tiling3(unitcube, self.bbox).translate(Vector3(4,4,4)).map(n,n,n,n)
        self.assertTrue(t.proximate(t1))
