from math import sqrt
from random import random


class Vector3():

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "Vector3(%f, %f, %f)"%(self.x, self.y, self.z)
        
    def __hash__(self):
        return hash((Vector3, self.x, self.y, self.z))
        
    def __getitem__(self, n):
        if n == 1:
            return self.x
        elif n == 2:
            return self.y
        elif n == 3:
            return self.z
        else:
            raise IndexError("Vector3 has components 1, 2, 3 only.")

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, s):
        return Vector3(s*self.x, s*self.y, s*self.z)

    def __div__(self, s):
        return Vector3(self.x/s, self.y/s, self.z/s)

    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)
    
    def dot(self, other):
        return self.x*other.x + self.y*other.y + self.z*other.z
    
    def norm(self):
        return sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
    
    def distance(self, other):
        return (self-other).norm()

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z


def random_norm1():
    """
    A random vector on the unit sphere.
    """
    while True:
        # A point uniformly distributed in the box [-1,1] * [-1,1] * [-1,1]
        v = Vector3(random()*2-1, random()*2-1, random()*2-1)
        n = v.norm()
        # We restrict to points inside the unit sphere so as to get
        # points of uniformly distributed direction, and reject points
        # with tiny norm because we're worried about dividing by zero.
        if n < 1.0 and n > 0.01:
            return v/n
