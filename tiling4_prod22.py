from tiling4 import Tiling4
from vector4 import Vector4

def cartesian_product(t1, t2):
    """
    Takes the cartesian product of two Tiling2's.
    """
    
    def v00(v1,v2):
        return Vector4(v1.x, v1.y, v2.x, v2.y)

    def e10(e,v):
        (x,y) = e
        return frozenset([v00(x,v), v00(y,v)])

    def e01(v,e):
        (x,y) = e
        return frozenset([v00(v,x), v00(v,y)])

    def f20(f, v):
        return frozenset(frozenset([v00(x,v), v00(y,v)]) for (x,y) in f)
    
    def f11(e1, e2):
        return frozenset([e10(e1, x) for x in e2] +
                         [e01(x, e2) for x in e1])

    def f02(v, f):
        return frozenset(frozenset([v00(v,x), v00(v,y)]) for (x,y) in f)

    def g21(f, e):
        return frozenset([f11(e1,e) for e1 in f] +
                         [f20(f,v) for v in e])

    def g12(e, f):
        return frozenset([f11(e,e1) for e1 in f] +
                         [f02(v,f) for v in e])

    def h22(f1, f2):
        return frozenset([g21(f1,e) for e in f2] +
                         [g12(e,f2) for e in f1])

    vertices = {}
    for (v1,a1) in t1.vertices.iteritems():
        for (v2,a2) in t2.vertices.iteritems():
            vertices[v00(v1,v2)] = (0,a1,0,a2)

    edges = {}
    for (e,a1) in t1.edges.iteritems():
        for (v,a2) in t2.vertices.iteritems():
            edges[e10(e,v)] = (1,a1,0,a2)
    for (v,a1) in t1.vertices.iteritems():
        for (e,a2) in t2.edges.iteritems():
            edges[e01(v,e)] = (0,a1,1,a2)

    faces = {}
    for (f,a1) in t1.faces.iteritems():
        for (v,a2) in t2.vertices.iteritems():
            faces[f20(f,v)] = (2,a1,0,a2)
    for (e1,a1) in t1.edges.iteritems():
        for (e2,a2) in t2.edges.iteritems():
            faces[f11(e1,e2)] = (1,a1,1,a2)
    for (v,a1) in t1.vertices.iteritems():
        for (f,a2) in t2.faces.iteritems():
            faces[f02(v,f)] = (0,a1,2,a2)

    volumes = {}
    for (f,a1) in t1.faces.iteritems():
        for (e,a2) in t2.edges.iteritems():
            volumes[g21(f,e)] = (2,a1,1,a2)
    for (e,a1) in t1.edges.iteritems():
        for (f,a2) in t2.faces.iteritems():
            volumes[g12(e,f)] = (1,a1,2,a2)

    hypervolumes = {}
    for (f1,a1) in t1.faces.iteritems():
        for (f2,a2) in t2.faces.iteritems():
            hypervolumes[h22(f1,f2)] = (2,a1,2,a2)

    return Tiling4(vertices, edges, faces, volumes, hypervolumes)

