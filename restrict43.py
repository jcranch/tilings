from tiling3 import Tiling3
from vector3 import Vector3


def restrict43(t):
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
        if v.w == 0:
            raise ValueError("Vertex %s lies in cell w=0"%(v,)) # Check Cell is the right word.

    newv = {}
    for (e,x) in t.edges.iteritems():
        (v1,v2) = e
        if v2.w < 0 < v1.w:
            (v1,v2) = (v2,v1)
        if v1.w < 0 < v2.z:
            # If the edge passes through the plane z=0, then the
            # result will contain a vertex lying at the point of
            # intersection.
            u1 = Vector3(v1.x, v1.y, v1.z)
            u2 = Vector3(v2.x, v2.y, v2.z)
            newv[e] = ((u1*(v2.w) - u2*(v1.w))/(v2.w - v1.w), x)   # Need to check this!

    newe = {}
    for (f,x) in t.faces.iteritems():
        e = frozenset(newv[e1][0] for e1 in f if e1 in newv)
        if e:
            newe[f] = (e,x)

    newf = {}
    for (g,x) in t.volumes.iteritems():
        f = frozenset(newe[f1][0] for f1 in g if f1 in newe)
        if f:
            newf[f] = (f,x)
            
    newg = {}
    for (h,x) in t.hypervolumes.iteritems(): # check syntax
        g = frozenset(newe[f1][0] for f1 in h if f1 in newe)
        if g:
            newg[g] = x
            
    return Tiling3(newv.itervalues(), newe.itervalues(), newf.itervalues(), newg)
