from math import sin, cos
from random import random

from vector2 import Vector2


class Matrix2():

    def __init__(self, l):
        ((a,b),(c,d)) = l
        self.array = ((a,b),(c,d))

    def __repr__(self):
        return "Matrix2([[%f, %f], [%f, %f]])"%(tuple(self[(i,j)] for i in [1,2] for j in [1,2]))

    def __getitem__(self, (r, s)):
        return self.array[r-1][s-1]

    def __add__(self, other):
        return Matrix2([[self[(i,j)]+other[(i,j)] for j in [1,2]] for i in [1,2]])

    def __mul__(self, other):
        "Matrix multiplication"
        return Matrix2([[sum(self[(i,k)]*other[(k,j)] for k in [1,2]) for j in [1,2]] for i in [1,2]])

    def __call__(self, other):
        "Matrix acting on a vector"
        [a,b] = [sum(self[(i,j)]*other[j] for j in [1,2]) for i in [1,2]]
        return Vector2(a,b)

    def row(self,i):
        return Vector2(self[(1,i)], self[(2,i)])

    def column(self,j):
        return Vector2(self[(j,1)], self[(j,2)])

    def determinant(self):
        ((a,b),(c,d)) = self.array
        return a*d - b*c


def rotation(theta):
    return Matrix2([[cos(theta),sin(theta)],[-sin(theta),cos(theta)]])


def random_special_orthogonal():
    return rotation(random()*2*pi)
