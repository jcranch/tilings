from vector3 import *
from matrix3 import Matrix3
from math import sqrt

class Vector3Tests(unittest.TestCase):
    
    def test_calculations(self):
        v1 = Vector3(1,2,3)
        v2 = Vector3(1,0,0)
        v3 = Vector3(0,0,0)
        v4 = Vector3(0,sqrt(3)/2,0)
        self.assertEqual(v.norm() , sqrt(v.dot(v)))    
        self.assertEqual((v/v.norm()).norm(), 1)
        self.assertEqual(v.distance(v), 0)
        self.assertEqual(triangle3_area(v2,v3,v4),sqrt(3)/4)
               
    def test_type(self):
        v1 = Vector3(3,4,5)
        v2 = Vector3(6,7,8)
        m = Matrix3([[1,1,1],[2,2,2],[3,3,3]])
        self.assertTrue(isinstance(v1.cross(v2),Vector3))
        self.assertTrue(isinstance(v1*10, Vector3))
        self.assertTrue(isinstance(v1/10, Vector3))
        self.assertTrue(isinstance(v1+v2, Vector3))
        self.assertTrue(isinstance(v1-v2, Vector3))
        self.assertTrue(isinstance(m(v1), Vector3))
        self.assertTrue(isinstance(v1.dot(v2), float))
     
    def test_raise_errors(self):
        v1 = Vector3(2,2,6)        
        with self.assertRaises(IndexError):
            v1[0] 
        with self.assertRaises(IndexError):
            v1[4]            
        self.assertEqual(v1[2],2)
