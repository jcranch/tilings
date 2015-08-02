import unittest

from permutations import *


class TestPermutations(unittest.TestCase):

    def permutations(self,n):
        orig = list(xrange(1,n+1))

        count_evens = 0
        evens = set()

        count_odds = 0
        odds = set()

        for (s1,p) in permutations_with_sign(orig):
            if s1 == 1:
                count_evens += 1
                evens.add(p)
            elif s1 == -1:
                count_odds += 1
                odds.add(p)
            else:
                self.fail("sign isn't +1 or -1")

            # Is the sign right?
            s2 = 1
            for i in xrange(n-1):
                for j in xrange(i+1,n):
                    if p[i]>p[j]:
                        s2 = -s2

            self.assertEqual(s1,s2)

        fact = 1
        for i in xrange(1,n+1):
            fact *= i

        # Should be the right number of each and they should all be different
        self.assertEqual(count_evens, fact//2)
        self.assertEqual(len(evens), fact//2)
        self.assertEqual(count_odds, fact//2)
        self.assertEqual(len(odds), fact//2)

    def test_perm2(self):
        self.permutations(4)

    def test_perm4(self):
        self.permutations(4)

    def test_perm5(self):
        self.permutations(4)
