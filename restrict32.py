from tiling2 import Tiling2
from vector2 import Vector2
#I'm struggling to understand what this function is doing. Can you enlighten me by answering these questions I've added?
#Are we trying to take a 3D tiling and 2D Tiling  and produce a 2D tile to represent the intersection with distances between verticies preserved from 3D to 2D?


def restrict32(t):
    """
    Restrict a Tiling3 to a Tiling2 (by taking z coordinate = 0).

    For now, it complains if any vertices lie in the intersection
    (this should be a measure-zero event...)
    """
    
    for (v,x) in t.vertices.iteritems():
        if v.z == 0:
            raise ValueError("Vertex %s lies in plane z=0"%(v,))

    newv = {}
    for (e,x) in t.edges.iteritems():
        (v1,v2) = e
        if v2.z < 0 < v1.z:
            (v1,v2) = (v2,v1)
        if v1.z < 0 < v2.z:
            u1 = Vector2(v1.x, v1.y)
            u2 = Vector2(v2.x, v2.y)
            newv[e] = ((u1*(v2.z) - u2*(v1.z))/(v2.z - v1.z), x) #I am confused at what this line is doing geometrically. Please can you explain?

    newe = {}
    for (f,x) in t.faces.iteritems():
        e = frozenset(newv[e1][0] for e1 in f if e1 in newv)
        if e:
            newe[f] = (e,x)

    newf = {}
    for (g,x) in t.volumes.iteritems():
        f = frozenset(newe[f1][0] for f1 in g if f1 in newe)
        if f:
            newf[f] = x
            
    return Tiling2(newv.itervalues(), newe.itervalues(), newf)
