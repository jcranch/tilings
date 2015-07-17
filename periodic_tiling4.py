from common import LatticeSearcher
from vector4 import Vector4
from tiling4 import Tiling4

def periodic_tiling4(fundamental_vertices, fundamental_edges,
                     fundamental_faces, fundamental_volumes,fundamental_hypervolumes,
                     bounding_box,
                     period_vectors = [Vector4(1,0,0,0), Vector4(0,1,0,0), Vector4(0,0,1,0),Vector4(0,0,0,1)]):

    """
    Build a periodic tiling.
    The fundamental geometric features are given as dicts. For
    fundamental_vertices, the keys are labels, and the values are
    vectors. For the rest, the keys are labels, and the values are
    lists of pairs whose first element is the label of something of
    dimension one less, and whose second element is a tuple of
    coefficients of the period vectors.
    The extent of the structure is found by adding and subtracting the
    elements of period_vectors from the given vertices, while still
    remaining inside the box.
    In the resulting tiling, the labels are pairs: one is a label, and
    the other is a tuple of coefficients of the period vectors.
    """

    ((minw,maxw),(minx, maxx), (miny, maxy), (minz, maxz)) = bounding_box
    
    n = len(period_vectors) # 4 for a space-filling tiling, but let's not assume

    vertices = {}
    for (label, v0) in fundamental_vertices.iteritems():

        if minw > v0.w or maxw < v0.w or minx > v0.x or maxx < v0.x or miny > v0.y or maxy < v0.y or minz > v0.z or maxz < v0.z:
            raise ValueError("The bounding box should contain the fundamental domain")
        
        gen = LatticeSearcher(n)
        for coeffs in gen:
            v = sum((u*c for (c,u) in zip(coeffs, period_vectors)), v0)
            if minw <= v.w <= maxw and minx <= v.x <= maxx and miny <= v.y <= maxy and minz <= v.z <= maxz:
                vertices[(label,coeffs)] = v
            else:
                gen.reject()

    def tsum(t1,t2):
        return tuple(x+y for (x,y) in zip(t1,t2))
                
    edges = {}
    for (label, vs) in fundamental_edges.iteritems():
        gen = LatticeSearcher(n)
        for coeffs in gen:
            s = [(a,tsum(coeffs,offset)) for (a,offset) in vs]
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

    volumes = {}
    for (label, fs) in fundamental_volumes.iteritems():
        gen = LatticeSearcher(n)
        for coeffs in gen:
            s = [(a,tsum(coeffs,offset)) for (a,offset) in fs]
            if all(f in faces for f in s):
                volumes[(label,coeffs)] = frozenset(faces[f] for f in s)
            else:
                gen.reject()

                
    hypervolumes = {}
    for (label, gs) in fundamental_hypervolumes.iteritems():
        gen = LatticeSearcher(n)
        for coeffs in gen:
            s = [(a,tsum(coeffs,offset)) for (a,offset) in gs]
            if all(g in volumes for g in s):
                hypervolumes[(label,coeffs)] = frozenset(volumes[g] for g in s)
            else:
                gen.reject()  
                
                
    v = dict((x,l) for (l,x) in vertices.iteritems())
    e = dict((x,l) for (l,x) in edges.iteritems())
    f = dict((x,l) for (l,x) in faces.iteritems())
    g = dict((x,l) for (l,x) in volumes.iteritems())
    h = dict((x,l) for (l,x) in hypervolumes.iteritems())
    
    return Tiling4(v,e,f,g,h)
