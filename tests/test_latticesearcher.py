import unittest

from periodic_tiling3 import LatticeSearcher


class LatticeSearcherTest(unittest.TestCase):

    def test_diamond(self):
        """
        Uses the LatticeSearcher to find all lattice points (x,y) with
        |x|+|y| at most 4.
        """
        
        a = []
        g = LatticeSearcher(2)
        for (x,y) in g:
            if abs(x)+abs(y) > 4:
                g.reject()
            else:
                a.append((x,y))

        self.assertEqual(len(a), 41)
