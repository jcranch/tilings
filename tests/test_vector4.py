from vector4 import *
from matrix4 import Matrix4
from math import sqrt

class Vector4Tests(unittest.TestCase):
    
    def test_calculations(self):
        v1 = Vector4(1,2,3,4)
        self.assertAlmostEqual(v1.norm() , sqrt(v1.dot(v1)))    
        self.assertAlmostEqual((v1/v1.norm()).norm(), 1)
        self.assertAlmostEqual(v1.distance(v1), 0)
               
    def test_type(self):
        v1 = Vector4(3,4,5,1)
        v2 = Vector4(6,7,8,9)
        m = Matrix4([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])
        self.assertTrue(isinstance(v1*10, Vector4))
        self.assertTrue(isinstance(v1/10, Vector4))
        self.assertTrue(isinstance(v1+v2, Vector4))
        self.assertTrue(isinstance(v1-v2, Vector4))
        self.assertTrue(isinstance(m(v2), Vector4))
        self.assertTrue(isinstance(v1.dot(v2), float))
     
    def test_raise_errors(self):
        v1 = Vector4(1,2,6,5)        
        with self.assertRaises(IndexError):
            v1[0] 
        with self.assertRaises(IndexError):
            v1[5]            
        self.assertEqual(v1[2],2)
