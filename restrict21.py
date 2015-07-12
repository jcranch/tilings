from tiling1 import Tiling1


def restrict21(t):
    """
    Given a Tiling2, produce the Tiling1 corresponding to the
    cross-section consisting of the line with y coordinate = 0.

    For now, it complains if any vertices have y = 0. Of course, this
    should be a measure-zero event, and can be avoided by small
    translations. This makes the algorithm much simpler: edges in the
    input produce vertices in the output, and faces in the input
    produce edges in the output.
    """
    
    for (v,a) in t.vertices.iteritems():
        if v.y == 0:
            raise ValueError("Vertex %s lies in plane z=0"%(v,))

    newv = {}
    for (e,a) in t.edges.iteritems():
        (v1,v2) = e
        if v2.y < 0 < v1.y:
            (v1,v2) = (v2,v1)
        if v1.y < 0 < v2.y:
            # If the edge passes through the line y=0, then the
            # result will contain a vertex lying at the point of
            # intersection.
            newv[e] = ((v1.x*(v2.y) - v2.x*(v1.y))/(v2.y - v1.y), a)

    newe = {}
    for (f,x) in t.faces.iteritems():
        e = frozenset(newv[e1][0] for e1 in f if e1 in newv)
        if e:
            newe[e] = x
            
    return Tiling1(newv.itervalues(), newe)
