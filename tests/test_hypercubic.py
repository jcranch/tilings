from unittest import TestCase, skip

from vector4 import Vector4
from tiling4_periodic import cubic_tiling4, simple_periodic_tiling4
from tiling4_polytope import hypercube


class Hypercubic(TestCase):

    def test_simple_periodic(self):
        b = ((-2.5, 1.5), (-1.5, 2.5), (-2.5, 1.5), (-1.5, 2.5))
        c = hypercube(((0,1), (0,1), (0,1), (0,1)))
        n = lambda x: None
        t1 = simple_periodic_tiling4(c, b).map(n,n,n,n,n)
        t2 = cubic_tiling4(b).map(n,n,n,n,n)
        self.assertTrue(t1.proximate(t2))
