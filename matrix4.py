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


def triangle4_area(v0, v1, v2):
    a = v1-v0
    b = v2-v0
    l = [a.w*b.x - a.x-b.w,
         a.w*b.y - a.y-b.w,
         a.w*b.z - a.z-b.w,
         a.x*b.y - a.y-b.x,
         a.x*b.z - a.z-b.x,
         a.y*b.z - a.z-b.y]
    return sqrt(sum(t*t for t in l))/2.0

def tetra4_volume(v0, v1, v2, v3):
    a = v1-v0
    b = v2-v0
    c = v3-v0
    return Vector4(  a.x*b.y*c.z - a.x*b.z*c.y + a.z*b.x*c.y
                   - a.z*b.y*c.x + a.y*b.z*c.x - a.y*b.x*c.z,
                     a.w*b.y*c.z - a.w*b.z*c.y + a.z*b.w*c.y
                   - a.z*b.y*c.w + a.y*b.z*c.w - a.y*b.w*c.z,
                     a.x*b.w*c.z - a.x*b.z*c.w + a.z*b.x*c.w
                   - a.z*b.w*c.x + a.w*b.z*c.x - a.w*b.x*c.z,
                     a.x*b.y*c.w - a.x*b.w*c.y + a.w*b.x*c.y
                   - a.w*b.y*c.x + a.y*b.w*c.x - a.y*b.x*c.w).norm()/6.0

def pentatope4_hypervolume(v0, v1, v2, v3, v4):
    return Matrix4([v1-v0, v2-v0, v3-v0, v4-v0]).determinant()/24.0
