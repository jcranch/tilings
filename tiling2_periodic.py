from common import LatticeSearcher
from vector2 import Vector2
from tiling2 import Tiling2


def periodic_tiling2(fundamental_vertices, fundamental_edges,
                     fundamental_faces,
                     bounding_box,
                     period_vectors = [Vector2(1,0), Vector2(0,1)]):

    """
    -Build a periodic tiling.
    The fundamental geometric features are given as dicts. For
    fundamental_vertices, the keys are labels, and the values are
    vectors.

    -For the rest, the keys are labels, and the values are
    lists of pairs whose first element is the label of something of
    dimension one less, and whose second element is a tuple of
    coefficients of the period vectors.

    -The extent of the structure is found by adding and subtracting the
    elements of period_vectors from the given vertices, while still
    remaining inside the box.

    -In the resulting tiling, the labels are pairs: one is a label, and
    the other is a tuple of coefficients of the period vectors.

    """

    ((minx, maxx), (miny, maxy)) = bounding_box

    n = len(period_vectors) # 2 for a space-filling tiling, but let's not assume

    vertices = {}
    for (label, v0) in fundamental_vertices.iteritems():

        if minx > v0.x or maxx < v0.x or miny > v0.y or maxy < v0.y :
            raise ValueError("The bounding box should contain the fundamental domain")

        gen = LatticeSearcher(n)
        for coeffs in gen: #using the lattices generated as co-efficients of periodic vectors!
            v = sum((u*c for (c,u) in zip(coeffs, period_vectors)), v0)
            if minx <= v.x <= maxx and miny <= v.y <= maxy:
                vertices[(label,coeffs)] = v #If this new vector lies within the bounday box, keep it and add it to verticies
            else:
                gen.reject() #if not reject it! This makes sure we don't go n forever (with constant vectors).

    def tsum(t1,t2):
        return tuple(x+y for (x,y) in zip(t1,t2))

    edges = {}
    for (label, vs) in fundamental_edges.iteritems():
        gen = LatticeSearcher(n)
        for coeffs in gen:
            s = [(a,tsum(coeffs,offset)) for (a,offset) in vs]
            # Take vertices that form the edge. a is the label of the vertex, offset is the l.c. of the period vectors.
            # So this takes the fundamental edge and adds it to some valid vertex and sees
            if all(v in vertices for v in s):
                edges[(label,coeffs)] = frozenset(vertices[v] for v in s)
            else:
                gen.reject()

    faces = {}
    for (label, es) in fundamental_faces.iteritems():
        gen = LatticeSearcher(n)
        for coeffs in gen:
            s = [(a,tsum(coeffs,offset)) for (a,offset) in es]
            if all(e in edges for e in s):
                faces[(label,coeffs)] = frozenset(edges[e] for e in s)
            else:
                gen.reject()


    v = dict((x,l) for (l,x) in vertices.iteritems())
    e = dict((x,l) for (l,x) in edges.iteritems())
    f = dict((x,l) for (l,x) in faces.iteritems())

    return Tiling2(v,e,f)





def cubic_tiling2(bounding_box):

    v = {(): Vector2(0,0)} #The fundamental vertex.

    e = {(1,): [((), (0,0)), ((), (1,0))], #unitx
         (2,): [((), (0,0)), ((), (0,1))]} #unity

    f = {(1,2): [((1,), (0,0)), ((2,), (0,0)),
                 ((1,), (0,1)), ((2,), (1,0))]}

    return periodic_tiling2(v,e,f,bounding_box)


def triangular_tiling(bounding_box):
    periods = [Vector2(1,0),Vector2(0.5,3**0.5/2)] # _ and /
    fundamental_vertex = {(): Vector2(0,0)}
    fundamental_edges = {(1,):[((),(0,0)), ((),(0,1))], #/
                         (2,):[((),(0,0)), ((),(1,0))], #-
                         (3,):[((),(0,1)),((),(1,0))]}  #\
    fundamental_faces = {True:[((1,),(0,0)),((2,),(0,0)),((3,),(0,0))],
                         False:[((1,),(1,0)),((2,),(0,1)),((3,),(0,0))]}
    return periodic_tiling2(fundamental_vertex,fundamental_edges,fundamental_faces,bounding_box,periods)


def hexagonal_tiling(bounding_box):
    periods = [Vector2(0,3**0.5), Vector2(1.5,3**0.5/2)]
    fundamental_vertices = {True: Vector2(0,0),   # >-
                            False: Vector2(1,0)}  # -<
    fundamental_edges = {1:[(True, (0,0)), (False, (0,0))],
                         2:[(True, (0,0)), (False, (0,-1))],
                         3:[(True, (0,0)), (False, (1,-1))]}
    fundamental_faces = {():[(1,(0,0)), (2,(0,1)), (3,(0,1)),
                             (1,(1,0)), (2,(1,0)), (3,(0,0))]}
    return periodic_tiling2(fundamental_vertices,fundamental_edges,
                            fundamental_faces,bounding_box,periods)


def simple_union(tiling2s, epsilon=1e-7):
    """
    Fits together a bunch of Tiling2 objects which approximately share
    vertices, edges, faces, etc. Preserves labelling without
    complaining about mismatches.
    """

    d = {}
    dvals = set()
    vertices = {}
    edges = {}
    faces = {}
    
    for t in tiling2s:
        for v in t.vertices:
            for u in dvals:
                if u.distance(v) < epsilon:
                    d[v] = u
                    break
            else:
                dvals.add(v)
                d[v] = v

        for (v,x) in t.vertices.iteritems():
            vertices[d[v]] = x

        for (e,x) in t.edges.iteritems():
            edges[frozenset(d[v] for v in e)] = x

        for (f,x) in t.faces.iteritems():
            faces[frozenset(frozenset(d[v] for v in e) for e in f)] = x

    return Tiling2(vertices, edges, faces)


def periodic_copies(tiling2, bounding_box,
                    periods=[Vector2(1,0), Vector2(0,1)]):
    gen = LatticeSearcher(len(periods))
    for n in gen:
        t1 = tiling2.translate(sum((u*c for (u,c) in zip(periods, n)), Vector2(0,0)))
        if t1.in_box(bounding_box):
            yield t1
        else:
            gen.reject()

            
def simple_periodic_tiling2(tiling2, bounding_box,
                            periods=[Vector2(1,0), Vector2(0,1)]):
                
    return simple_union(periodic_copies(tiling2, bounding_box, periods))
