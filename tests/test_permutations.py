import unittest

from permutations import *


class TestPermutations(unittest.TestCase):

    def test_permutations(self):
        s = [1,2,3,4,5]
        a = list(all_permutations(s))
        self.assertEqual(len(a), 120)
        b = set(tuple(r) for r in all_permutations(s))
        self.assertEqual(len(b), 120)

    def test_even_permutations(self):
        s = [1,2,3,4,5]
        a = list(even_permutations(s))
        self.assertEqual(len(a), 120//2)
        b = set(tuple(r) for r in even_permutations(s))
        self.assertEqual(len(b), 120//2)
