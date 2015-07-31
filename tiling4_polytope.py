from tiling4 import Tiling4
from vector4 import Vector4
from matrix4 import Matrix4, pentatope_hypervolume
from matrix3 import Matrix3


def tiling4_polytope(dict_vertices, list_edges, list_faces, list_volumes,list_hypervolumes):
    """
    This function is designed to help make Tiling4 objects
    corresponding to polytopes.
    dict_vertices should be a dictionary with Vector4 objects
    as values.
    list_edges should be a list of lists where each sublists contains
    two labels of vertices which corresponds to the edge defined by
    joining those vertices; similarly for list_faces, list_volumes and list_hypervolumes.
    """
    dict_vertices = dict(dict_vertices)
    list_edges = list(list_edges)
    list_faces = list(list_faces)
    list_volumes = list(list_volumes)
    list_of_hypervolumes = list(list_hypervolumes)
    
    # We reverse the keys and values for now and change them at the end.
    dict_edges = {}
    for edge in list_edges:
        s = frozenset(edge)
        dict_edges[s] = frozenset(dict_vertices[k] for k in edge)

    dict_faces = {}
    for face in list_faces:
        s = frozenset(v for e in face for v in e)
        dict_faces[s] = frozenset(dict_edges[frozenset(k)] for k in face)
    
    
    dict_volumes = {}
    for volume in list_volumes:
        s = frozenset(v for f in volume for v in f)
        dict_volumes[s] = frozenset(dict_faces[frozenset(k)] for k in volume)
    
    
    hypervolumes = {}
    for hypervolume in list_hypervolumes:
        s = frozenset(v for g in hypervolume for v in g)
        hypervolumes[frozenset(dict_volumes[frozenset(k)] for k in hypervolume)] = s  
        
    # Now we reverse the keys and values to correct position for a tiling4.
    vertices = ((k,v) for (v,k) in dict_vertices.iteritems())
    edges = ((k,v) for (v,k) in dict_edges.iteritems())
    faces = ((k,v) for (v,k) in dict_faces.iteritems())
    volumes = ((k,v) for (v,k) in dict_volumes.iteritems())
    
    return Tiling4(vertices, edges, faces, volumes, hypervolumes)


def tiling4_convex_hull(vertices, epsilon=1e-7):
    """
    Takes a dictionary of vertices, and creates a polyhedron given by
    the convex hull.
    """
    vertices = dict(vertices)
    l_vertices = list(vertices)
     
    def cocellular(h,i,j,k):
        """
        Find the vertices in the same cell (3d space) as vertices h,i,j,k.
        If any occur before k, then we bale out as we should have
        already considered this cell.
        We calculate by considering the hypervolume of the pentatope
        formed by vertices h,i,j,k and one other. If (close to) zero,
        the five points are cocellular. If positive, the other point is
        on one side of the cell, and if negative it's on the
        other. Hence we bale out if we find points on both sides of
        the cell.  
        """
        t = l_vertices[h]
        u = l_vertices[i] 
        v = l_vertices[j]
        w = l_vertices[k]  

        side1 = False
        side2 = False
        for r in range(0,h)+range(h+1,i)+range(i+1,j)+range(j+1,k): 
            x = l_vertices[r] 
            a = pentatope_hypervolume(t,u,v,w,x) 
            if abs(a) < epsilon: 
                return None
            elif a < 0: 
                if side2: 
                    return None
                side1 = True 
            else:
                if side1: 
                    return None
                side2 = True
        level = [t,u,v,w] 
        for r in range(k+1,n): 
            x = l_vertices[r]
            a = pentatope_hypervolume(t,u,v,w,x)
            if abs(a) < epsilon:
                level.append(x) 
            elif a < 0:
                if side2:
                    return None
                side1 = True
            else:
                if side1:
                    return None
                side2 = True
        return level 
    
    # Produce the volumes: they're the maximal subsets of cocellular
    # vertices, with the property that every other vertex is on the
    # same side.    
    n = len(l_vertices)
    volumes = []
    for h in xrange(n-3): 
        for i in xrange(h+1,n-2): 
            for j in xrange(i+1,n-1):
                for k in xrange(j+1,n):
                    level = cocellular(h,i,j,k) 
                    if level is None: 
                        continue 
                    volumes.append(frozenset(level)) 

    # The faces are the intersections of the volumes that have at
    # least 3 vertices in common, and the edges are those that have
    # two vertices in common.
    faces = set()
    n = len(volumes)
    for i in xrange(0,n-1): 
        for j in xrange(i+1,n):
            a = volumes[i].intersection(volumes[j]) 
            if len(a) > 2:
                faces.add(a)

    edges = set()
    lfaces = list(faces)
    n = len(faces)
    for i in xrange(0,n-1): 
        for j in xrange(i+1,n):
            a = lfaces[i].intersection(lfaces[j]) 
            if len(a) == 2:
                edges.add(a)
                
    # Now we need the rest of the data in the preferred form
    edges = [frozenset(vertices[v] for v in e) for e in edges]
    faces = [frozenset(vertices[v] for v in f) for f in faces]
    volumes = [frozenset(vertices[v] for v in g) for g in volumes]
    hypervolumes = [volumes]
    
    volumes = [set(f for f in faces if f.issubset(g)) for g in volumes] 
    faces = [set(e for e in edges if e.issubset(f)) for f in faces]
    
    vertices = dict((v,k) for (k,v) in vertices.iteritems())

    return tiling4_polytope(vertices, edges, faces, volumes, hypervolumes)


def pentatope():
    root5 = 5**0.5
    dictionary_of_vertices = {
        Vector4(1, 1, 1, -1/root5): 0,
        Vector4(1, -1, -1, -1/root5): 1,
        Vector4(-1, 1, -1, -1/root5): 2,
        Vector4(-1, -1, 1, -1/root5): 3,
        Vector4(0, 0, 0, root5 - 1/root5): 4 }
    return tiling4_convex_hull(dictionary_of_vertices)


def hypercube():
    vertices = [Vector4(w,x,y,z)
                for w in [-1,1] for x in [-1,1] for y in [-1,1] for z in [-1,1]]
    return tiling4_convex_hull(dict(zip(vertices, xrange(16))))


def decahexahedroid():
    dictionary_of_vertices = {
        Vector4(1, 0, 0, 0): 0,
        Vector4(0, 1, 0, 0): 1,
        Vector4(0, 0, 1, 0): 2,
        Vector4(0, 0, 0, 1): 3,
        Vector4(-1, 0, 0, 0): 4,
        Vector4(0, -1, 0, 0): 5,
        Vector4(0, 0, -1, 0): 6,
        Vector4(0, 0, 0, -1): 7 }
    return tiling4_convex_hull(dictionary_of_vertices)




