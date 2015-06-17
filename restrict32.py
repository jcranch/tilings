from tiling2 import Tiling2
from vector2 import Vector2


def restrict32(t):
    """
    Given a Tiling3, produce the Tiling2 corresponding to the
    cross-section consisting of the plane with z coordinate = 0.

    For example, if t is a cubic tiling, translated a little, then the
    result will be a square tiling.

    If you want a different plane cross-section, you've got to rotate
    and translate the tiling first.

    For now, it complains if any vertices have z = 0. Of course, this
    should be a measure-zero event, and can be avoided by small
    translations. This makes the algorithm much simpler: edges in the
    input produce vertices in the output; faces in the input produce
    edges in the output, and volumes in the input produce faces in the
    output.
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
            # If the edge passes through the plane z=0, then the
            # result will contain a vertex lying at the point of
            # intersection.
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
