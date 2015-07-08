from math import sin, cos

from vector3 import Vector3, random_norm1


class Matrix3():

    def __init__(self, l):
        ((a,b,c),(d,e,f),(g,h,i)) = l
        self.array = ((a,b,c),(d,e,f),(g,h,i))

    def __repr__(self):
        return "Matrix3([[%f, %f, %f], [%f, %f, %f], [%f, %f, %f]])"%(tuple(self[(i,j)] for i in [1,2,3] for j in [1,2,3]))
        
    def __getitem__(self, (r, s)):
        return self.array[r-1][s-1]

    def __add__(self, other):
        return Matrix3([[self[(i,j)]+other[(i,j)] for j in [1,2,3]] for i in [1,2,3]])

    def __mul__(self, other):
        "Matrix multiplication"
        return Matrix3([[sum(self[(i,k)]*other[(k,j)] for k in [1,2,3]) for j in [1,2,3]] for i in [1,2,3]])

    def __call__(self, other):
        "Matrix acting on a vector"
        [a,b,c] = [sum(self[(i,j)]*other[j] for j in [1,2,3]) for i in [1,2,3]]
        return Vector3(a,b,c)

    def row(self,i):
        return Vector3(self[(1,i)], self[(2,i)], self[(3,i)])

    def column(self,j):
        return Vector3(self[(j,1)], self[(j,2)], self[(j,3)])

    def determinant(self):
        ((a,b,c),(d,e,f),(g,h,i)) = self.array
        return a*(e*i-f*h) + b*(f*g-d*i) + c*(d*h-e*g)



def rotate_x(theta):
    return Matrix3([[1,0,0],[0,cos(theta),sin(theta)],[0,-sin(theta),cos(theta)]])

def rotate_y(theta):
    return Matrix3([[cos(theta),0,sin(theta)],[0,1,0],[-sin(theta),0,cos(theta)]])

def rotate_z(theta):
    return Matrix3([[cos(theta),sin(theta),0],[-sin(theta),cos(theta),0],[0,0,1]])

def random_orthogonal():
    u = random_norm1()
    v0 = random_norm1()
    v1 = v0-u*(u.dot(v0))
    v = v1/(v1.norm())
    w0 = random_norm1()
    w1 = w0-u*(u.dot(w0))-v*(v.dot(w0))
    w = w1/(w1.norm())
    return Matrix3([u,v,w])

def random_special_orthogonal():
    u = random_norm1()
    v0 = random_norm1()
    v1 = v0-u*(u.dot(v0))
    v = v1/(v1.norm())
    w0 = random_norm1()
    w1 = w0-u*(u.dot(w0))-v*(v.dot(w0))
    w = w1/(w1.norm())
    m = Matrix3([u,v,w])
    if m.determinant() < 0:
        return Matrix3([u,v,-w])
    else:
        return m
