from math import sqrt
from random import random


class Vector4(object):

    def __init__(self, w, x, y, z):
        self.w = float(w)
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __repr__(self):
        return "Vector4(%f, %f, %f, %f)"%(self.w, self.x, self.y, self.z)

    def __hash__(self):
        return hash((Vector4, self.w, self.x, self.y, self.z))

    def __getitem__(self, n):
        if n == 1:
            return self.w
        elif n == 2:
            return self.x
        elif n == 3:
            return self.y
        elif n == 4:
            return self.z
        else:
            raise IndexError("Vector4 has components 1, 2, 3, 4 only.")

    def __add__(self, other):
        return Vector4(self.w + other.w, self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector4(self.w - other.w, self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, s):
        return Vector4(s*self.w, s*self.x, s*self.y, s*self.z)

    def __truediv__(self, s):
        return Vector4(self.w/s, self.x/s, self.y/s, self.z/s)

    def __neg__(self):
        return Vector4(-self.w,-self.x, -self.y, -self.z)

    def dot(self, other):
        return self.w*other.w + self.x*other.x + self.y*other.y + self.z*other.z

    def norm(self):
        return sqrt(self.w*self.w + self.x*self.x + self.y*self.y + self.z*self.z)

    def distance(self, other):
        return (self-other).norm()

    def __iter__(self):
        yield self.w
        yield self.x
        yield self.y
        yield self.z

    def in_box(self, box):
        ((minw, maxw), (minx, maxx), (miny, maxy), (minz, maxz)) = box
        return (minw <= self.w <= maxw) and (minx <= self.x <= maxx) and (miny <= self.y <= maxy) and (minz <= self.z <= maxz)


def random_norm1_4():
    """
    A random vector on the unit sphere.
    """
    while True:
        # A point uniformly distributed in the box [-1,1] * [-1,1] * [-1,1]
        v = Vector4(random()*2-1, random()*2-1, random()*2-1,random()*2-1)
        n = v.norm()
        # We restrict to points inside the unit sphere so as to get
        # points of uniformly distributed direction, and reject points
        # with tiny norm because we're worried about dividing by zero.
        if n < 1.0 and n > 0.01:
            return v/n
