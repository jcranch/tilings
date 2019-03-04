from tiling3 import Tiling3
from vector3 import Vector3


def restrict43(t):
    """
    Given a Tiling4, produce the Tiling3 corresponding to the
    cross-section consisting of the hyperplane with z coordinate = 0.
    For example, if t is a tiling of hypercubes, translated a little,
    then the result will be a cubic tiling.
    If you want a different hyperplane cross-section, you've got to
    rotate and translate the tiling first.

    For now, it complains if any vertices have z = 0. Of course, this
    should be a measure-zero event, and can be avoided by small
    translations. This makes the algorithm much simpler: edges in the
    input produce vertices in the output; faces in the input produce
    edges in the output, volumes in the input produce faces in the
    output, and hypervolumes in the input produce volumes in the
    output.
    """

    for (v,x) in t.vertices.items():
        if v.z == 0:
            raise ValueError("Vertex %s lies in cell z=0"%(v,)) # Check Cell is the right word.

    newv = {}
    for (e,l) in t.edges.items():
        (v1,v2) = e
        if v2.z < 0 < v1.z:
            (v1,v2) = (v2,v1)
        if v1.z < 0 < v2.z:
            # If the edge passes through the plane z=0, then the
            # result will contain a vertex lying at the point of
            # intersection.
            u1 = Vector3(v1.w, v1.x, v1.y)
            u2 = Vector3(v2.w, v2.x, v2.y)
            newv[e] = ((u1*(v2.z) - u2*(v1.z))/(v2.z - v1.z), l)

    newe = {}
    for (f,x) in t.faces.items():
        e = frozenset(newv[e1][0] for e1 in f if e1 in newv)
        if e:
            newe[f] = (e,x)

    newf = {}
    for (g,x) in t.volumes.items():
        f = frozenset(newe[f1][0] for f1 in g if f1 in newe)
        if f:
            newf[g] = (f,x)

    newg = {}
    for (h,x) in t.hypervolumes.items():
        g = frozenset(newf[g1][0] for g1 in h if g1 in newf)
        if g:
            newg[h] = (g,x)

    return Tiling3(newv.values(), newe.values(), newf.values(), newg.values())
