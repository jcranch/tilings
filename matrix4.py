from math import sin, cos

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

