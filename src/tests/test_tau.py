import unittest

from tau import tau


class TauTest(unittest.TestCase):

    def test_arithmetic(self):

        a = tau*3 - 2
        b = tau*5 - 7
        c = 8
        d = 8.3

        self.assertAlmostEqual(float(a+b), float(a)+float(b))
        self.assertAlmostEqual(float(a+c), float(a)+float(c))
        self.assertAlmostEqual(float(a+d), float(a)+float(d))
        self.assertAlmostEqual(float(a-b), float(a)-float(b))
        self.assertAlmostEqual(float(a-c), float(a)-float(c))
        self.assertAlmostEqual(float(a-d), float(a)-float(d))
        self.assertAlmostEqual(float(a*b), float(a)*float(b))
        self.assertAlmostEqual(float(a*c), float(a)*float(c))
        self.assertAlmostEqual(float(a*d), float(a)*float(d))
        self.assertAlmostEqual(float(b+a), float(b)+float(a))
        self.assertAlmostEqual(float(c+a), float(c)+float(a))
        self.assertAlmostEqual(float(d+a), float(d)+float(a))
        self.assertAlmostEqual(float(b-a), float(b)-float(a))
        self.assertAlmostEqual(float(c-a), float(c)-float(a))
        self.assertAlmostEqual(float(d-a), float(d)-float(a))
        self.assertAlmostEqual(float(b*a), float(b)*float(a))
        self.assertAlmostEqual(float(c*a), float(c)*float(a))
        self.assertAlmostEqual(float(d*a), float(d)*float(a))
