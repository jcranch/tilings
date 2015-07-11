from tiling3 import Tiling3
from vector3 import Vector3



def tiling3_polyhedron(dictionary_of_vertices, list_of_edges, list_of_faces, list_of_volumes):
    '''
    This function is designed to help make Tiling3 objects
    corresponding to polyhedra.

    dictionary_of_vertices should be a dictionary with keys that are
    distinct labels of the form (1,), (2,), ... (m,) respectively and
    values that are Vector3(x,y,z) for x,y,z that are co-ordinates of
    given vertex.

    list_of_edges should be a list of lists where each sublists
    contains two labels of vertices which corresponds to the edge
    defined by joining those vertices and similarly for faces and
    volumes.
    '''
    # First we make the items of our new dictionaries ready for a tiling3 input.
    items_of_edges = []
    for edge in list_of_edges:
        list_of_vertices_auxiliary = []
        for vertex in edge:
            list_of_vertices_auxiliary += sorted([vertex][0])
        items_of_edges += [tuple(sorted(set(list_of_vertices_auxiliary)))]
    items_of_faces = []
    for face in list_of_faces:
        list_of_edges_auxiliary = []
        for edge in face:
            list_of_edges_auxiliary += sorted([edge][0])
        items_of_faces += [tuple(sorted(set(list_of_edges_auxiliary)))]
    items_of_volumes = []
    for volume in list_of_volumes:
        list_of_faces_auxiliary = []
        for face in volume:
            list_of_faces_auxiliary += sorted([face][0])
        items_of_volumes += [tuple(sorted(set(list_of_faces_auxiliary)))]
    # Now we make the corresponding keys. 
    # We reverse the keys and values for now and change them at the end.
    keys_of_edges = []
    for edge in list_of_edges:
        keys_of_edges += [frozenset([dictionary_of_vertices[tuple(sorted(k))] for k in sorted(edge)])]
    dictionary_of_edges = dict([[item[1],item[0]] for item in zip(keys_of_edges,items_of_edges)])
    
    keys_of_faces = []
    for face in list_of_faces:
        keys_of_faces += [frozenset([dictionary_of_edges[tuple(sorted(k))] for k in sorted(face)])]
    dictionary_of_faces = dict([[item[1],item[0]] for item in zip(keys_of_faces,items_of_faces)])  
    
    keys_of_volumes = []
    for volume in list_of_volumes:
        keys_of_volumes += [frozenset([dictionary_of_faces[tuple(sorted(k))] for k in sorted(volume)])]
    
    # Now we reverse the keys and values to correct position for a tiling3 input.
    dictionary_of_vertices =  dict (zip(dictionary_of_vertices.values(),dictionary_of_vertices.keys()))
    dictionary_of_edges = dict([[item[0],item[1]] for item in zip(keys_of_edges,items_of_edges)])
    dictionary_of_faces = dict([[item[0],item[1]] for item in zip(keys_of_faces,items_of_faces)]) 
    dictionary_of_volumes = dict([[item[0],item[1]] for item in zip(keys_of_volumes,items_of_volumes)])
    
    return Tiling3(dictionary_of_vertices,dictionary_of_edges,dictionary_of_faces,dictionary_of_volumes)
    
def tetrahedron():
    dict_of_vertices = {(1,):Vector3(1, 1, 1),
                        (2,):Vector3(-1, -1, 1),
                        (3,):Vector3(-1, 1, -1),
                        (4,):Vector3(1, -1, -1)}

    edges = [[(1,),(2,)],[(1,),(4,)],[(1,),(3,)],
             [(3,),(4,)],[(2,),(3,)],[(2,),(4,)]]
    faces = [[(1,2),(2,4),(1,4)],[(1,3),(3,4),(1,4)],
             [(2,3),(3,4),(2,4)],[(1,2),(2,3),(1,3)]]
    volumes = [[(1,2,4),(1,3,4),(2,3,4),(1,2,3)]]

    return tiling3_polyhedron(dict_of_vertices,edges,faces,volumes)

def cube():
    dictionary_of_vertices = {(1,):Vector3(-1,-1,-1),(2,):Vector3(1,-1,-1),(3,):Vector3(1,1,-1),(4,):Vector3(-1,1,-1),
                              (5,):Vector3(-1,-1,1),(6,):Vector3(1,-1,1),(7,):Vector3(1,1,1),(8,):Vector3(-1,1,1)}
    list_of_edges = [[(1,),(2,)],[(2,),(3,)],[(3,),(4,)],[(4,),(1,)],
                     [(1+4,),(2+4,)],[(2+4,),(3+4,)],[(3+4,),(4+4,)],[(4+4,),(1+4,)],
                     [(1,),(5,)],[(2,),(6,)],[(3,),(7,)],[(4,),(8,)]]
    list_of_faces = [[(1,2),(2,3),(3,4),(4,1)],
                     [(1+4,2+4),(2+4,3+4),(3+4,4+4),(4+4,1+4)],
                     [(1,2),(2,6),(6,5),(5,1)],
                     [(4,3),(7,3),(7,8),(4,8)],
                     [(1,4),(4,8),(8,5),(5,1)],
                     [(6,2),(2,3),(3,7),(7,6)]]
    list_of_volumes = [[(1,2,3,4),(5,6,7,8),
                        (1,2,6,5),(4,3,7,8),
                        (1,4,8,5),(2,3,7,6)]]
    return tiling3_polyhedron(dictionary_of_vertices, list_of_edges, list_of_faces, list_of_volumes)

def octahedron():
    dictionary_of_vertices = {(1,):Vector3(-1,0,0),
                        (2,):Vector3(0,1,0),
                        (3,):Vector3(1,0,0),
                        (4,):Vector3(0,-1,0),
                        (5,):Vector3(0,0,1),
                        (6,):Vector3(0,0,-1)}

    list_of_edges = [[(1,),(2,)],[(2,),(3,)],[(3,),(4,)],[(1,),(4,)],
             [(1,),(5,)],[(1,),(6,)],[(2,),(5,)],[(2,),(6,)],
             [(3,),(5,)],[(3,),(6,)],[(4,),(5,)],[(4,),(6,)]]

    list_of_faces = [[(1,2),(1,6),(2,6)], [(1,4),(1,6),(4,6)],
             [(3,4),(3,6),(4,6)], [(2,3),(2,6),(3,6)],
             [(1,2),(1,5),(2,5)], [(1,4),(1,5),(4,5)],
             [(3,4),(3,5),(4,5)], [(2,3),(2,5),(3,5)]]

    list_of_volumes = [[(1,2,6),(1,4,6),(3,4,6),(2,3,6),
                (1,2,5),(1,4,5),(3,4,5),(2,3,5)]]

    return tiling3_polyhedron(dictionary_of_vertices, list_of_edges, list_of_faces, list_of_volumes)

def dodecahedron():
    phi = (1 + 5**0.5)/2
    iphi = (1-5**0.5)/2
    dictionary_of_vertices = {
    (1,):Vector3(-1,-1,-1), (2,):Vector3(1,-1,-1),(3,):Vector3(1,1,-1),(4,):Vector3(-1,1,-1),
    (5,):Vector3(-1,-1,1), (6,):Vector3(1,-1,1),(7,):Vector3(1,1,1),(8,):Vector3(-1,1,1),
    (9,):Vector3(iphi,0,-phi), (10,):Vector3(-iphi,0,-phi),(11,):Vector3(iphi,0,phi),(12,):Vector3(-iphi,0,phi),
    (13,):Vector3(-phi,iphi,0), (14,):Vector3(-phi,-iphi,0),(15,):Vector3(phi,iphi,0),(16,):Vector3(phi,-iphi,0),
    (17,):Vector3(0,-phi,iphi), (18,):Vector3(0,-phi,-iphi),(19,):Vector3(0,phi,iphi),(20,):Vector3(0,phi,-iphi)}

    list_of_edges = [
    [(1,),(9,)],[(4,),(9,)],[(2,),(10,)],[(3,),(10,)],[(10,),(9,)],
    [(5,),(11,)],[(8,),(11,)],[(6,),(12,)],[(7,),(12,)],[(11,),(12,)],

    [(1,),(13,)],[(5,),(13,)],[(4,),(14,)],[(8,),(14,)],[(13,),(14,)],
    [(2,),(15,)],[(6,),(15,)],[(3,),(16,)],[(7,),(16,)],[(15,),(16,)],

    [(1,),(17,)],[(2,),(17,)],[(5,),(18,)],[(6,),(18,)],[(17,),(18,)],
    [(4,),(19,)],[(3,),(19,)],[(8,),(20,)],[(7,),(20,)],[(19,),(20,)]]

    list_of_faces = [

    [(1,17),(17,2),(1,9),(2,10),(9,10)], 
    [(3,19),(4,19),(4,9),(3,10),(9,10)], 

    [(11,5),(5,18),(18,6),(6,12),(11,12)], 
    [(12,7),(7,20),(20,8),(8,11),(11,12)], 

    [(13,5),(5,11),(11,8),(8,14),(13,14)], 
    [(13,1),(1,9),(9,4),(4,14),(13,14)], 

    [(16,7),(7,12),(12,6),(6,15),(15,16)], 
    [(16,3),(3,10),(10,2),(2,15),(15,16)], 

    [(18,5),(5,13),(13,1),(1,17),(17,18)], 
    [(17,2),(2,15),(15,6),(6,18),(17,18)], 

    [(19,3),(3,16),(7,16),(7,20),(19,20)], 
    [(19,4),(4,14),(14,8),(8,20),(19,20)]]

    list_of_volumes = [[
    (1,2,9,10,17),
    (3,4,9,10,19),

    (5,6,11,12,18),
    (7,8,11,12,20),

    (5,8,11,13,14),
    (1,4,9,13,14),

    (6,7,12,15,16),
    (2,3,10,15,16),

    (1,5,13,17,18),
    (2,6,15,17,18),

    (3,7,16,19,20),
    (4,8,14,19,20)]]
    return tiling3_polyhedron(dictionary_of_vertices, list_of_edges, list_of_faces, list_of_volumes)

def icosahedron():
    phi = (1 + 5**0.5)/2
    dictionary_of_vertices = {
    (1,):Vector3(0,-1,phi), (2,):Vector3(phi,0,1),(3,):Vector3(1,phi,0),(4,):Vector3(-1,phi,0),
    (5,):Vector3(-phi,0,1), (6,):Vector3(0,1,phi),(7,):Vector3(1,-phi,0),(8,):Vector3(phi,0,-1),
    (9,):Vector3(0,1,-phi), (10,):Vector3(-phi,0,-1),(11,):Vector3(-1,-phi,0),(12,):Vector3(0,-1,-phi)}

    list_of_edges = [
    [(1,),(6,)],[(2,),(6,)],[(3,),(6,)],[(4,),(6,)],[(5,),(6,)],
    [(1,),(2,)],[(2,),(3,)],[(3,),(4,)],[(4,),(5,)],[(1,),(5,)],

    [(1+6,),(6+6,)],[(2+6,),(6+6,)],[(3+6,),(6+6,)],[(4+6,),(6+6,)],[(5+6,),(6+6,)],
    [(1+6,),(2+6,)],[(2+6,),(3+6,)],[(3+6,),(4+6,)],[(4+6,),(5+6,)],[(1+6,),(5+6,)],

    [(1,),(7,)],[(2,),(7,)],[(2,),(8,)],[(3,),(8,)],[(3,),(9,)],
    [(4,),(9,)],[(4,),(10,)],[(5,),(10,)],[(5,),(11,)],[(1,),(11,)]]

    list_of_faces = [

    [(1,6),(1,2),(2,6)],
    [(2,6),(2,3),(3,6)],
    [(3,6),(3,4),(4,6)],
    [(4,6),(4,5),(5,6)],
    [(1,6),(1,5),(5,6)],


    [(1+6,6+6),(1+6,2+6),(2+6,6+6)],
    [(2+6,6+6),(2+6,3+6),(3+6,6+6)],
    [(3+6,6+6),(3+6,4+6),(4+6,6+6)],
    [(4+6,6+6),(4+6,5+6),(5+6,6+6)],
    [(1+6,6+6),(1+6,5+6),(5+6,6+6)],

    [(1,2),(1,7),(2,7)], 
    [(2,3),(2,8),(3,8)], 
    [(3,4),(3,9),(4,9)], 
    [(4,5),(4,10),(5,10)], 
    [(1,5),(5,11),(1,11)], 

    [(7,8),(7,2),(8,2)], 
    [(8,9),(8,3),(9,3)], 
    [(9,10),(9,4),(10,4)], 
    [(10,11),(5,10),(5,11)], 
    [(11,7),(7,1),(1,11)]]

    list_of_volumes = [[
    (1,2,6),(2,3,6),(3,4,6),(4,5,6),(1,5,6),

    (1+6,2+6,6+6),(2+6,3+6,6+6),(3+6,4+6,6+6),(4+6,5+6,6+6),(1+6,5+6,6+6),

    (1,2,7),(2,3,8),(3,4,9),(4,5,10),(1,5,11),

    (2,7,8),(3,8,9),(4,9,10),(5,10,11),(1,7,11)]]
    return tiling3_polyhedron(dictionary_of_vertices, list_of_edges, list_of_faces, list_of_volumes)
