from tiling4 import Tiling4


def tiling4_pointset(vertices, proto_hypervolumes, epsilon=1e-7):
    """
    Creates a Tiling4 by recognising isomorphic copies of
    proto_hypervolumes among the vertices.

    Vertices should be a dict with Vector4 objects as values.

    proto_hypervolumes should be a list of tiling4 objects each
    with a single hypervolume.

    In practice, this is rather slow.
    """

    def extend(l, d, n):
        if n==len(l):
            yield d
        else:
            u = l[n]
            for v in vertices:
                if all(abs(u.distance(u1) - v.distance(v1)) < epsilon for (u1,v1) in d.iteritems()):
                    d0 = d.copy()
                    d0[l[n]] = v
                    for d1 in extend(l, d0, n+1):
                        yield d1

    edges = {}
    faces = {}
    volumes = {}
    hypervolumes = {}
                        
    for t in proto_hypervolumes:
        for d in extend(list(t.vertextour()), {}, 0):

            for e in t.edges:
                edges[frozenset(d[v] for v in e)] = None

            for f in t.faces:
                faces[frozenset(frozenset(d[v] for v in e) for e in f)] = None

            for g in t.volumes:
                volumes[frozenset(frozenset(frozenset(d[v] for v in e) for e in f) for f in g)] = None

            for (h,x) in t.hypervolumes.iteritems():
                hypervolumes[frozenset(frozenset(frozenset(frozenset(d[v] for v in e) for e in f) for f in g) for g in h)] = x
        
    return Tiling4(vertices, edges, faces, volumes, hypervolumes)
