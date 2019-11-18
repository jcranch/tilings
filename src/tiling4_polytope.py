from collections import defaultdict
from itertools import chain
import os
import time

from tiling4 import tiling4
from vector4 import Vector4
from matrix4 import tetra4_volume, pentatope4_hypervolume
from permutations import plus_minuses


autotilings_dir = "autotilings"

def tiling4_convex_hull(vertices, epsilon=1e-7, statusreport=False, max_volumes_per_vertex=None):
    """
    Takes a dictionary of vertices, and creates a polyhedron given by
    the convex hull.

    If max_volumes_per_vertex is set, only looks for that number of
    volumes around each vertex.
    """
    start_time = time.time()
    vertices = dict(vertices)
    l_vertices = list(vertices)
    n = len(l_vertices)
    volumes = []
    vcount = defaultdict(int)

    def cohyperplanar(h,i,j,k):
        """
        Find the vertices in the same hyperplane as vertices h,i,j,k.

        At the beginning, we bale out if these vertices already lie in
        some volume we've constructed already, and if the vertices are
        in fact coplanar.

        We calculate by considering the hypervolume of the pentatope
        formed by vertices h,i,j,k and one other. If (close to) zero,
        the five points are cohyperplanar. If positive, the other point is
        on one side of the cell, and if negative it's on the
        other. We bale out if we find points on both sides of the cell.
        """
        level = set([h,i,j,k])

        if any(level.issubset(s) for s in volumes):
            return None

        t = l_vertices[h]
        u = l_vertices[i]
        v = l_vertices[j]
        w = l_vertices[k]

        if abs(tetra4_volume(t,u,v,w)) < epsilon:
            return None

        side1 = False
        side2 = False
        for r in chain(range(0,h), range(h+1,i), range(i+1,j), range(j+1,k), range(k+1,n)):
            x = l_vertices[r]
            a = pentatope4_hypervolume(t,u,v,w,x)
            if abs(a) < epsilon:
                level.add(r)
            elif a < 0:
                if side2:
                    return None
                side1 = True
            else:
                if side1:
                    return None
                side2 = True
        return level

    def gotenough(i):
        return max_volumes_per_vertex is not None and vcount[i] >= max_volumes_per_vertex

    # Produce the volumes: they're the maximal subsets of cohyperplanar
    # vertices, with the property that every other vertex is on the
    # same side.
    for h in range(n-3):
        if gotenough(h):
            continue
        for i in range(h+1,n-2):
            if gotenough(i):
                continue
            for j in range(i+1,n-1):
                if gotenough(j):
                    continue
                for k in range(j+1,n):
                    if gotenough(k):
                        continue
                    level = cohyperplanar(h,i,j,k)
                    if level is not None:
                        volumes.append(level)
                        if statusreport:
                            elapsed = time.time() - start_time
                            hours, elapsed = divmod(elapsed, 3600)
                            minutes, elapsed = divmod(elapsed, 60)
                            seconds, elapsed = divmod(elapsed, 1)
                            print("  found %d volumes (after %02d:%02d:%02d.%02d)"%(len(volumes), int(hours), int(minutes), int(seconds), int(elapsed*100)))
                        for x in level:
                            vcount[x] += 1
                        if gotenough(j) or gotenough(i) or gotenough(h):
                            break
                if gotenough(i) or gotenough(h):
                    break
            if gotenough(h):
                break
    volumes = [frozenset(vertices[l_vertices[i]] for i in l) for l in volumes]

    # The faces are the intersections of the volumes that have at
    # least 3 vertices in common, and the edges are those that have
    # two vertices in common.
    faces = set()
    n = len(volumes)
    for i in range(0,n-1):
        for j in range(i+1,n):
            a = volumes[i].intersection(volumes[j])
            if len(a) > 2:
                faces.add(a)

    edges = set()
    lfaces = list(faces)
    n = len(lfaces)
    for i in range(0,n-1):
        for j in range(i+1,n):
            a = lfaces[i].intersection(lfaces[j])
            if len(a) == 2:
                edges.add(a)

    # Now we need the rest of the data in the preferred form
    hypervolumes = [volumes]
    volumes = [set(f for f in faces if f.issubset(g)) for g in volumes]
    faces = [set(e for e in edges if e.issubset(f)) for f in faces]
    vertices = dict((v,k) for (k,v) in vertices.items())
    return tiling4(vertices, edges, faces, volumes, hypervolumes)

def tiling4_dual(tiling4):
    '''
    This function is designed for producing the duals of convex polytopes.
    '''
    dual_vertices = []
    for volume in tiling4.volumes:
        distinct_verticies = set()
        for face in volume :
            for edge in face:
                for vertex in edge:
                    distinct_verticies.add(vertex)
        sum_vertex = Vector4(0,0,0,0)
        for vertex in distinct_verticies :
            sum_vertex += vertex
        centroid = sum_vertex/len(distinct_verticies)
        dual_vertices.append(centroid)
    return tiling4_convex_hull(dict(zip(dual_vertices,range(len(dual_vertices)))))

def pentatope():
    root5 = 5**0.5
    dictionary_of_vertices = {
        Vector4(1, 1, 1, -1/root5): 0,
        Vector4(1, -1, -1, -1/root5): 1,
        Vector4(-1, 1, -1, -1/root5): 2,
        Vector4(-1, -1, 1, -1/root5): 3,
        Vector4(0, 0, 0, root5 - 1/root5): 4 }
    return tiling4_convex_hull(dictionary_of_vertices)

def hypercube(box=((-1,1),(-1,1),(-1,1),(-1,1))):
    (ws,xs,ys,zs) = box
    vertices = [Vector4(w,x,y,z) for w in ws for x in xs for y in ys for z in zs]
    return tiling4_convex_hull(dict(zip(vertices,range(16))))

def cell16():
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

def cell24():
    global autotilings_dir
    with open(os.path.join(autotilings_dir, "cell24.data"), 'r') as f:
        return(eval(f.read()))

def cell120():
    global autotilings_dir
    with open(os.path.join(autotilings_dir, "cell120.data"), 'r') as f:
        return(eval(f.read()))

def cell600():
    global autotilings_dir
    with open(os.path.join(autotilings_dir, "cell600.data"), 'r') as f:
        return(eval(f.read()))
