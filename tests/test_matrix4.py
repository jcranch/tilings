import unittest

from vector4 import Vector4
from matrix4 import pentatope4_hypervolume


class HypervolumeTest(unittest.TestCase):

    def test_coordinate_pentatope(self):
        a = Vector4(0,0,0,0)
        b = Vector4(1,0,0,0)
        c = Vector4(0,1,0,0)
        d = Vector4(0,0,1,0)
        e = Vector4(0,0,0,1)
        self.assertAlmostEqual(pentatope4_hypervolume(a,b,c,d,e), 1/24.0)
