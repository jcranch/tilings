from math import cos, sin, pi

from vector2 import Vector2
from tiling2 import Tiling2


def tiling2_polygon(vertices):
    """
    Vertices are a list of pairs, consisting of a label and a Vector2
    object.
    """
    v = dict((v,k) for (k,v) in vertices)
    e = dict((frozenset([u,v]),(k,l)) for ((k,u),(l,v)) in zip(vertices, vertices[1:]+[vertices[0]]))
    f = {frozenset(e): ()}
    return Tiling2(v,e,f)


def regular_polygon(n, radius=1.0, theta=0.0, centre=Vector2(0,0), grounded = False):
    if grounded:
        theta = -(n-2)*pi/(2*n)
    v = [(i, centre + Vector2(radius*cos(2*pi*i/n + theta),
                              radius*sin(2*pi*i/n + theta)))
         for i in range(n)]
    return tiling2_polygon(v)
