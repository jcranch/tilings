from tiling4 import Tiling4
from vector4 import Vector4




def tiling4_polytope(dictionary_of_vertices, list_of_edges, list_of_faces, list_of_volumes, list_of_hypervolumes):
    '''
    This function is designed to help make Tiling4 objects
    corresponding to polytopes.
    dictionary_of_vertices should be a dictionary with keys that are
    distinct labels of the form (1,), (2,), ... (m,) respectively and
    values that are Vector4(w,x,y,z) for w,x,y,z that are co-ordinates of
    given vertex.
    list_of_edges should be a list of lists where each sublists
    contains two labels of vertices which corresponds to the edge
    defined by joining those vertices and similarly for faces,
    volumes and hypervolumes.
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
    
    items_of_hypervolumes = []
    for hypervolume in list_of_hypervolumes:
        list_of_volumes_auxiliary = []
        for volume in hypervolume:
            list_of_volumes_auxiliary += [volume][0]
        items_of_hypervolumes += [tuple(set(list_of_volumes_auxiliary))]    
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
    dictionary_of_volumes = dict([[item[1],item[0]] for item in zip(keys_of_faces,items_of_volumes)])  
    
    keys_of_hypervolumes = []
    for hypervolume in list_of_hypervolumes:
        keys_of_hypervolumes += [frozenset([dictionary_of_volumes[k] for k in hypervolume])]
    dictionary_of_hypervolumes = dict([[item[1],item[0]] for item in zip(keys_of_volumes,items_of_hypervolumes)])    
    
    # Now we reverse the keys and values to correct position for a tiling3 input.
    dictionary_of_vertices =  dict (zip(dictionary_of_vertices.values(),dictionary_of_vertices.keys()))
    dictionary_of_edges = dict([[item[0],item[1]] for item in zip(keys_of_edges,items_of_edges)])
    dictionary_of_faces = dict([[item[0],item[1]] for item in zip(keys_of_faces,items_of_faces)]) 
    dictionary_of_volumes = dict([[item[0],item[1]] for item in zip(keys_of_volumes,items_of_volumes)])
    dictionary_of_hypervolumes = dict([[item[0],item[1]] for item in zip(keys_of_volumes,items_of_hypervolumes)])
    return Tiling4(dictionary_of_vertices,dictionary_of_edges,dictionary_of_faces,dictionary_of_volumes,dictionary_of_hypervolumes)
