from tiling2 import Tiling2
from vector2 import Vector2


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
            newv[e] = ((u1*(v2.z) - u2*(v1.z))/(v2.z - v1.z), x)

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
