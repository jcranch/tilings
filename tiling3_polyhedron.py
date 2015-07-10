from tiling3 import Tiling3
from vector3 import Vector3
from tiling3_matplotlib import matplotlib_display_tiling3



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
            list_of_vertices_auxiliary += [vertex][0]
        items_of_edges += [tuple(set(list_of_vertices_auxiliary))]

    items_of_faces = []
    for face in list_of_faces:
        list_of_edges_auxiliary = []
        for edge in face:
            list_of_edges_auxiliary += [edge][0]
        items_of_faces += [tuple(set(list_of_edges_auxiliary))]

    items_of_volumes = []
    for volume in list_of_volumes:
        list_of_faces_auxiliary = []
        for face in volume:
            list_of_faces_auxiliary += [face][0]
        items_of_volumes += [tuple(set(list_of_faces_auxiliary))]
    # Now we make the corresponding keys. 
    # We reverse the keys and values for now and change them at the end.
    keys_of_edges = []
    for edge in list_of_edges:
        keys_of_edges += [frozenset([dictionary_of_vertices[k] for k in edge])]
    dictionary_of_edges = dict([[item[1],item[0]] for item in zip(keys_of_edges,items_of_edges)])
    
    keys_of_faces = []
    for face in list_of_faces:
        keys_of_faces += [frozenset([dictionary_of_edges[k] for k in face])]
    dictionary_of_faces = dict([[item[1],item[0]] for item in zip(keys_of_faces,items_of_faces)])  
    
    keys_of_volumes = []
    for volume in list_of_volumes:
        keys_of_volumes += [frozenset([dictionary_of_faces[k] for k in volume])]
    
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



def octahedron():
    dict_of_vertices = {(1,):Vector3(-1,0,0),
                        (2,):Vector3(0,1,0),
                        (3,):Vector3(1,0,0),
                        (4,):Vector3(0,-1,0),
                        (5,):Vector3(0,0,1),
                        (6,):Vector3(0,0,-1)}

    edges = [[(1,),(2,)],[(2,),(3,)],[(3,),(4,)],[(1,),(4,)],
             [(1,),(5,)],[(1,),(6,)],[(2,),(5,)],[(2,),(6,)],
             [(3,),(5,)],[(3,),(6,)],[(4,),(5,)],[(4,),(6,)]]

    faces = [[(1,2),(1,6),(2,6)], [(1,4),(1,6),(4,6)],
             [(3,4),(3,6),(4,6)], [(2,3),(2,6),(3,6)],
             [(1,2),(1,5),(2,5)], [(1,4),(1,5),(4,5)],
             [(3,4),(3,5),(4,5)], [(2,3),(2,5),(3,5)]]

    volumes = [[(1,2,6),(1,4,6),(3,4,6),(2,3,6),
                (1,2,5),(1,4,5),(3,4,5),(2,3,5)]]

    return tiling3_polyhedron(dict_of_vertices,edges,faces,volumes)

