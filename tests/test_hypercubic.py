from unittest import TestCase, skip

from vector4 import Vector4
from periodic_tiling4 import cubic_tiling4
from tiling4_pointset import tiling4_pointset
from tiling4_polytope import hypercube


class CubicFromPointset(TestCase):

    @skip("takes too long to do routinely")
    def test_equality(self):

        n = lambda x: None
        p = cubic_tiling4(((-0.5,2.5), (-0.5,2.5), (-0.5,2.5), (-0.5,2.5))).map(n,n,n,n,n)
        a = dict((Vector4(w,x,y,z), None) for w in xrange(3) for x in xrange(3) for y in xrange(3) for z in xrange(3))
        x = hypercube().translate(Vector4(1,1,1,1)).scale(0.5)
        q = tiling4_pointset(a, [x]).map(n,n,n,n,n)
        self.assertTrue(p.proximate(q))

