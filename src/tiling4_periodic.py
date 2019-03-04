from common import LatticeSearcher
from vector4 import Vector4
from tiling4 import Tiling4
from tiling4_polytope import cell24


def periodic_tiling4(fundamental_vertices, fundamental_edges,
                     fundamental_faces, fundamental_volumes,
                     fundamental_hypervolumes,
                     bounding_box,
                     periods = [Vector4(1,0,0,0), Vector4(0,1,0,0),
                                Vector4(0,0,1,0), Vector4(0,0,0,1)]):

    """
    Build a periodic tiling.

    The fundamental geometric features are given as dicts. For
    fundamental_vertices, the keys are labels, and the values are
    vectors. For the rest, the keys are labels, and the values are
    lists of pairs whose first element is the label of something of
    dimension one less, and whose second element is a tuple of
    coefficients of the period vectors.

    The extent of the structure is found by adding and subtracting the
    elements of periods from the given vertices, while still
    remaining inside the box.

    In the resulting tiling, the labels are pairs: one is a label, and
    the other is a tuple of coefficients of the period vectors.
    """

    ((minw,maxw),(minx, maxx), (miny, maxy), (minz, maxz)) = bounding_box

    n = len(periods) # 4 for a space-filling tiling, but let's not assume

    vertices = {}
    for (label, v0) in fundamental_vertices.items():

        if (minw > v0.w or maxw < v0.w or
            minx > v0.x or maxx < v0.x or
            miny > v0.y or maxy < v0.y or
            minz > v0.z or maxz < v0.z):
            raise ValueError("The bounding box should contain the fundamental domain")

        gen = LatticeSearcher(n)
        for coeffs in gen:
            v = sum((u*c for (c,u) in zip(coeffs, periods)), v0)
            if minw <= v.w <= maxw and minx <= v.x <= maxx and miny <= v.y <= maxy and minz <= v.z <= maxz:
                vertices[(label,coeffs)] = v
            else:
                gen.reject()

    def tsum(t1,t2):
        return tuple(x+y for (x,y) in zip(t1,t2))

    edges = {}
    for (label, vs) in fundamental_edges.items():
        gen = LatticeSearcher(n)
        for coeffs in gen:
            s = [(a,tsum(coeffs,offset)) for (a,offset) in vs]
            if all(v in vertices for v in s):
                edges[(label,coeffs)] = frozenset(vertices[v] for v in s)
            else:
                gen.reject()

    faces = {}
    for (label, es) in fundamental_faces.items():
        gen = LatticeSearcher(n)
        for coeffs in gen:
            s = [(a,tsum(coeffs,offset)) for (a,offset) in es]
            if all(e in edges for e in s):
                faces[(label,coeffs)] = frozenset(edges[e] for e in s)
            else:
                gen.reject()

    volumes = {}
    for (label, fs) in fundamental_volumes.items():
        gen = LatticeSearcher(n)
        for coeffs in gen:
            s = [(a,tsum(coeffs,offset)) for (a,offset) in fs]
            if all(f in faces for f in s):
                volumes[(label,coeffs)] = frozenset(faces[f] for f in s)
            else:
                gen.reject()


    hypervolumes = {}
    for (label, gs) in fundamental_hypervolumes.items():
        gen = LatticeSearcher(n)
        for coeffs in gen:
            s = [(a,tsum(coeffs,offset)) for (a,offset) in gs]
            if all(g in volumes for g in s):
                hypervolumes[(label,coeffs)] = frozenset(volumes[g] for g in s)
            else:
                gen.reject()


    v = dict((x,l) for (l,x) in vertices.items())
    e = dict((x,l) for (l,x) in edges.items())
    f = dict((x,l) for (l,x) in faces.items())
    g = dict((x,l) for (l,x) in volumes.items())
    h = dict((x,l) for (l,x) in hypervolumes.items())

    return Tiling4(v,e,f,g,h)


def cubic_tiling4(bounding_box):

    v = {(): Vector4(0,0,0,0)} # Origin

    e = {(1,2): [((), (0,0,0,0)), ((), (1,0,0,0))],
         (1,4): [((), (0,0,0,0)), ((), (0,1,0,0))],
         (1,9): [((), (0,0,0,0)), ((), (0,0,1,0))],
         (1,5): [((), (0,0,0,0)), ((), (0,0,0,1))]}

    f = {

        (1,2,3,4): [((1,2), (0,0,0,0)), ((1,2), (0,1,0,0)),
                         ((1,4), (0,0,0,0)), ((1,4), (1,0,0,0))],

        (1,2,9,10): [((1,2), (0,0,0,0)), ((1,2), (0,0,1,0)),
                         ((1,9), (0,0,0,0)), ((1,9), (1,0,0,0))],

        (1,2,5,6): [((1,2), (0,0,0,0)), ((1,2), (0,0,0,1)),
                         ((1,5), (0,0,0,0)), ((1,5), (1,0,0,0))],

        (1,4,9,12): [((1,4), (0,0,0,0)), ((1,4), (0,0,1,0)),
                         ((1,9), (0,0,0,0)), ((1,9), (0,1,0,0))],

        (1,4,5,8): [((1,4), (0,0,0,0)), ((1,4), (0,0,0,1)),
                         ((1,5), (0,0,0,0)), ((1,5), (0,1,0,0))],

        (1,5,9,13): [((1,5), (0,0,0,0)), ((1,5), (0,0,1,0)),
                         ((1,9), (0,0,0,0)), ((1,9), (0,0,0,1))]}


    g = {
        (1,2,3,4,5,6,7,8): [((1,2,5,6), (0,0,0,0)), ((1,2,5,6), (0,1,0,0)),
                            ((1,4,5,8), (0,0,0,0)),((1,4,5,8), (1,0,0,0)),
                            ((1,2,3,4), (0,0,0,0)),((1,2,3,4), (0,0,0,1))],

        (1,2,5,6,9,10,13,14): [((1,2,5,6), (0,0,0,0)), ((1,2,5,6), (0,0,1,0)),
                            ((1,5,9,13), (0,0,0,0)),((1,5,9,13), (1,0,0,0)),
                            ((1,2,9,10), (0,0,0,0)),((1,2,9,10), (0,0,0,1))],

        (1,4,5,8,9,12,13,16): [((1,5,9,13), (0,0,0,0)), ((1,5,9,13), (0,1,0,0)),
                            ((1,4,9,12), (0,0,0,0)),((1,4,9,12), (0,0,0,1)),
                            ((1,4,5,8), (0,0,0,0)),((1,4,5,8), (0,0,1,0))],

        (1,2,3,4,9,10,11,12): [((1,2,3,4), (0,0,0,0)), ((1,2,3,4), (0,0,1,0)),
                            ((1,2,9,10), (0,0,0,0)),((1,2,9,10), (0,1,0,0)),
                            ((1,4,9,12), (0,0,0,0)),((1,4,9,12), (1,0,0,0))]}

    h = {(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16): [
        ((1,4,5,8,9,12,13,16),(0,0,0,0)),((1,4,5,8,9,12,13,16),(1,0,0,0)),
        ((1,2,5,6,9,10,13,14),(0,0,0,0)),((1,2,5,6,9,10,13,14),(0,1,0,0)),
        ((1,2,3,4,5,6,7,8),(0,0,0,0)),((1,2,3,4,5,6,7,8),(0,0,1,0)),
        ((1,2,3,4,9,10,11,12),(0,0,0,0)),((1,2,3,4,9,10,11,12),(0,0,0,1))]}

    return periodic_tiling4(v,e,f,g,h,bounding_box)


def simple_union(tiling4s, epsilon=1e-7):
    """
    Fits together a bunch of Tiling4 objects which approximately share
    vertices, edges, faces, etc. Preserves labelling without
    complaining about mismatches.
    """

    d = {}
    dvals = set()
    vertices = {}
    edges = {}
    faces = {}
    volumes = {}
    hypervolumes = {}

    for t in tiling4s:
        for v in t.vertices:
            for u in dvals:
                if u.distance(v) < epsilon:
                    d[v] = u
                    break
            else:
                dvals.add(v)
                d[v] = v

        for (v,x) in t.vertices.items():
            vertices[d[v]] = x

        for (e,x) in t.edges.items():
            edges[frozenset(d[v] for v in e)] = x

        for (f,x) in t.faces.items():
            faces[frozenset(frozenset(d[v] for v in e) for e in f)] = x

        for (g,x) in t.volumes.items():
            volumes[frozenset(frozenset(frozenset(d[v] for v in e) for e in f) for f in g)] = x

        for (h,x) in t.hypervolumes.items():
            hypervolumes[frozenset(frozenset(frozenset(frozenset(d[v] for v in e) for e in f) for f in g) for g in h)] = x

    return Tiling4(vertices, edges, faces, volumes, hypervolumes)


def periodic_copies(tiling4, bounding_box,
                    periods=[Vector4(1,0,0,0), Vector4(0,1,0,0),
                             Vector4(0,0,1,0), Vector4(0,0,0,1)]):
    gen = LatticeSearcher(len(periods))
    for n in gen:
        t1 = tiling4.translate(sum((u*c for (u,c) in zip(periods, n)), Vector4(0,0,0,0)))
        if t1.in_box(bounding_box):
            yield t1
        else:
            gen.reject()


def simple_periodic_tiling4(tiling4, bounding_box,
                            periods=[Vector4(1,0,0,0), Vector4(0,1,0,0),
                                     Vector4(0,0,1,0), Vector4(0,0,0,1)]):

    return simple_union(periodic_copies(tiling4, bounding_box, periods))


def cell24_tiling(box):

    periods = [Vector4(4, 0, 0, 0),
               Vector4(2, -2, 0, 0),
               Vector4(0, 2, -2, 0),
               Vector4(0, 0, 2, -2)]

    return simple_periodic_tiling4(cell24(), box, periods=periods)


def cell24_tiling_separate(box):

    periods = [Vector4(4, 0, 0, 0),
               Vector4(2, -2, 0, 0),
               Vector4(0, 2, -2, 0),
               Vector4(0, 0, 2, -2)]

    return list(periodic_copies(cell24(), box, periods=periods))
