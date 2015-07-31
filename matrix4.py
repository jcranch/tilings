from math import sin, cos
from matrix3 import Matrix3
from vector4 import Vector4


class Matrix4():

    def __init__(self, ll):
        ((a,b,c,d),(e,f,g,h),(i,j,k,l),(m,n,o,p)) = ll
        self.array = ((a,b,c,d),(e,f,g,h),(i,j,k,l),(m,n,o,p))

    def __getitem__(self, (r, s)):
        return self.array[r-1][s-1]

    def __add__(self, other):
        return Matrix4([[self[(i,j)]+other[(i,j)] for j in [1,2,3,4]] for i in [1,2,3,4]])

    def __mul__(self, other):
        "Matrix multiplication"
        return Matrix4([[sum(self[(i,k)]*other[(k,j)] for k in [1,2,3,4]) for j in [1,2,3,4]] for i in [1,2,3,4]])

    def __call__(self, other):
        "Matrix acting on a vector"
        [a,b,c,d] = [sum(self[(i,j)]*other[j] for j in [1,2,3,4]) for i in [1,2,3,4]]
        return Vector4(a,b,c,d)

    def determinant(self):
        ((a,b,c,d),(e,f,g,h),(i,j,k,l),(m,n,o,p)) = self.array 
        return a*Matrix3([[f,g,h],[j,k,l],[n,o,p]]).determinant() -\
               b*Matrix3([[e,g,h],[i,k,l],[m,o,p]]).determinant() +\
               c*Matrix3([[e,f,h],[i,j,l],[m,n,p]]).determinant() -\
               d*Matrix3([[e,f,g],[i,j,k],[m,n,o]]).determinant()

def rotate_wx(theta):
    return Matrix4([[1,0,0,0],[0,1,0,0],[0,0,cos(theta),sin(theta)],[0,0,-sin(theta),cos(theta)]])

def rotate_wy(theta):
    return Matrix4([[1,0,0,0],[0,cos(theta),0,sin(theta)],[0,0,1,0],[0,-sin(theta),0,cos(theta)]])

def rotate_wz(theta):
    return Matrix4([[1,0,0,0],[0,cos(theta),sin(theta),0],[0,-sin(theta),cos(theta),0],[0,0,0,1]])

def rotate_xy(theta):
    return Matrix4([[cos(theta),0,0,sin(theta)],[0,1,0,0],[0,0,1,0],[-sin(theta),0,0,cos(theta)]])

def rotate_xz(theta):
    return Matrix4([[cos(theta),0,sin(theta),0],[0,1,0,0],[-sin(theta),0,cos(theta),0],[0,0,0,1]])

def rotate_yz(theta):
    return Matrix4([[cos(theta),sin(theta),0,0],[-sin(theta),cos(theta),0,0],[0,0,1,0],[0,0,0,1]])


def pentatope_hypervolume(v0, v1, v2, v3, v4):
    return Matrix4([v1-v0, v2-v0, v3-v0, v4-v0]).determinant()/24.0
