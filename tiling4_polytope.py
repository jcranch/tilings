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
    
    items_of_hypervolumes = []
    for hypervolume in list_of_hypervolumes:
        list_of_volumes_auxiliary = []
        for volume in hypervolume:
            list_of_volumes_auxiliary += sorted([volume][0])
        items_of_hypervolumes += [tuple(sorted(set(list_of_volumes_auxiliary)))]    
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
    dictionary_of_volumes = dict([[item[1],item[0]] for item in zip(keys_of_volumes,items_of_volumes)])  
    
    keys_of_hypervolumes = []
    for hypervolume in list_of_hypervolumes:
        keys_of_hypervolumes += [frozenset([dictionary_of_volumes[tuple(sorted(k))] for k in sorted(hypervolume)])]
    dictionary_of_hypervolumes = dict([[item[1],item[0]] for item in zip(keys_of_hypervolumes,items_of_hypervolumes)])    
    
    # Now we reverse the keys and values to correct position for a tiling3 input.
    dictionary_of_vertices =  dict (zip(dictionary_of_vertices.values(),dictionary_of_vertices.keys()))
    dictionary_of_edges = dict([[item[0],item[1]] for item in zip(keys_of_edges,items_of_edges)])
    dictionary_of_faces = dict([[item[0],item[1]] for item in zip(keys_of_faces,items_of_faces)]) 
    dictionary_of_volumes = dict([[item[0],item[1]] for item in zip(keys_of_volumes,items_of_volumes)])
    dictionary_of_hypervolumes = dict([[item[0],item[1]] for item in zip(keys_of_hypervolumes,items_of_hypervolumes)])
    return Tiling4(dictionary_of_vertices,dictionary_of_edges,dictionary_of_faces,dictionary_of_volumes,dictionary_of_hypervolumes)

def hypercube():
    dictionary_of_vertices = {
(1,):Vector4(-1.0,-1.0,-1.0,-1.0),(2,):Vector4(1.0,-1.0,-1.0,-1.0),(3,):Vector4(1.0,1.0,-1.0,-1.0),(4,):Vector4(-1.0,1.0,-1.0,-1.0),
(9,):Vector4(-1.0,-1.0,1.0,-1.0),(10,):Vector4(1.0,-1.0,1.0,-1.0),(11,):Vector4(1.0,1.0,1.0,-1.0),(12,):Vector4(-1.0,1.0,1.0,-1.0),

(5,):Vector4(-1.0,-1.0,-1.0,1.0),(6,):Vector4(1.0,-1.0,-1.0,1.0),(7,):Vector4(1.0,1.0,-1.0,1.0),(8,):Vector4(-1.0,1.0,-1.0,1.0),
(13,):Vector4(-1.0,-1.0,1.0,1.0),(14,):Vector4(1.0,-1.0,1.0,1.0),(15,):Vector4(1.0,1.0,1.0,1.0),(16,):Vector4(-1.0,1.0,1.0,1.0)}
    
    list_of_edges = [
[(1,),(2,)],[(2,),(3,)],[(3,),(4,)],[(1,),(4,)],
[(5,),(6,)],[(6,),(7,)],[(7,),(8,)],[(5,),(8,)],

[(1,),(5,)],[(2,),(6,)],[(3,),(7,)],[(4,),(8,)],

[(9,),(10,)],[(10,),(11,)],[(11,),(12,)],[(12,),(9,)],
[(13,),(14,)],[(14,),(15,)],[(15,),(16,)],[(16,),(13,)],

[(9,),(13,)],[(10,),(14,)],[(11,),(15,)],[(12,),(16,)],

[(1,),(9,)],[(2,),(10,)],[(3,),(11,)],[(4,),(12,)],

[(5,),(13,)],[(6,),(14,)],[(7,),(15,)],[(8,),(16,)]]

    list_of_faces = [
[(1,2),(2,6),(6,5),(5,1)], #(1,2,5,6)
[(4,3),(3,7),(7,8),(8,4)], #(3,4,7,8)
[(9,10),(10,14),(14,13),(13,9)] , #(9,10,13,14)
[(12,11),(11,15),(15,16),(16,12)], #(11,12,15,16)

[(5,6),(6,14),(14,13),(13,5)], #(5,6,13,14)
[(8,7),(7,15),(15,16),(16,8)], #(7,8,15,16)
[(1,2),(2,10),(10,9),(9,1)], #(1,2,9,10)
[(4,3),(3,11),(11,12),(12,4)], #(3,4,11,12)

[(1,2),(2,3),(3,4),(1,4)], #(1,2,3,4)
[(5,6),(6,7),(7,8),(8,5)], #(5,6,7,8)

[(9,10),(10,11),(11,12),(9,12)], #(9,10,11,12)
[(13,14),(14,15),(15,16),(13,16)], #(13,14,15,16)

[(1,4),(4,12),(12,9),(9,1)], #(1,4,9,12)
[(2,3),(3,11),(11,10),(10,2)], #(2,3,10,11)

[(5,8),(8,16),(16,13),(13,5)], #(5,8,13,16)
[(6,7),(7,15),(15,14),(14,6)], #(6,7,14,15)

[(1,9),(9,13),(5,13),(1,5)], #(1,5,9,13)
[(2,10),(10,14),(6,14),(2,6)], #(2,6,10,14)

[(4,12),(12,16),(16,8),(8,4)], #(4,8,12,16)
[(3,11),(11,15),(15,7),(7,3)], #(3,7,11,15)

[(1,4),(4,8),(8,5),(1,5)], #(1,4,5,8)
[(2,3),(3,7),(7,6),(2,6)], #(2,3,6,7)

[(10,11),(11,15),(15,14),(10,14)], #(10,11,14,15)
[(9,12),(12,16),(16,13),(9,13)]] #(9,12,13,16)


    list_of_volumes = [
[(1,2,5,6),(3,4,7,8),
 (1,4,5,8),(2,3,6,7), 
 (1,2,3,4),(5,6,7,8)], #(1,2,3,4,5,6,7,8)

[(9,10,13,14),(11,12,15,16),
 (9,12,13,16),(10,11,14,15),
 (9,10,11,12),(13,14,15,16)], #(9,10,11,12,13,14,15,16)

[(1,2,5,6),(9,10,13,14),
 (1,5,9,13),(2,6,10,14),
 (1,2,9,10),(5,6,13,14)], #(1,2,5,6,9,10,13,14)

[(3,4,7,8),(11,12,15,16),
 (4,8,12,16),(3,7,11,15),
 (3,4,11,12),(7,8,15,16)], #(3,4,7,8,11,12,15,16)

[(1,4,5,8),(9,12,13,16),
 (1,5,9,13),(4,8,12,16),
 (1,4,9,12),(5,8,13,16)], #(1,4,5,8,9,12,13,16)

[(2,3,6,7),(10,11,14,15),
 (2,6,10,14),(3,7,11,15),
 (2,10,3,11),(6,7,14,15)], #(2,3,6,7,10,11,14,15)

[(5,8,13,16),(6,7,14,15),
 (5,6,7,8),(13,14,15,16),
 (5,6,13,14),(7,8,15,16)], #(5,6,7,8,13,14,15,16)

[(1,2,3,4),(9,10,11,12),
 (1,4,9,12),(2,3,10,11),
 (1,2,9,10),(3,4,11,12)]] #(1,2,3,4,9,10,11,12)

    
    list_of_hypervolumes = [
[(1,2,3,4,5,6,7,8),(9,10,11,12,13,14,15,16),(1,2,5,6,9,10,13,14),(3,4,7,8,11,12,15,16),
 (1,4,5,8,9,12,13,16),(2,3,6,7,10,11,14,15),(5,6,7,8,13,14,15,16),(1,2,3,4,9,10,11,12)]]
    
    return tiling4_polytope(dictionary_of_vertices,list_of_edges,list_of_faces,list_of_volumes,list_of_hypervolumes)


def pentatope():
    dictionary_of_vertices = {
(0,):Vector4(1.0,1.0,1.0,-1.0/(5**0.5)),(1,):Vector4(1.0,-1.0,-1.0,-1.0/(5**0.5)),(2,):Vector4(-1.0,1.0,-1.0,-1.0/(5**0.5)),
(3,):Vector4(-1.0,-1.0,1.0,-1.0/(5**0.5)),(4,):Vector4(0.0,0.0,0.0,5**0.5-1.0/(5**0.5))}
    
    list_of_edges = [
[(0,),(1,)],[(0,),(2,)],[(0,),(3,)],[(0,),(4,)],
[(1,),(2,)],[(1,),(3,)],[(1,),(4,)],
[(2,),(3,)],[(2,),(4,)],
[(3,),(4,)]]

    list_of_faces = [
[(0,1),(1,2),(0,2)], #(0,1,2)
[(0,1),(1,3),(0,3)], #(0,1,3)
[(0,1),(1,4),(0,4)], #(0,1,4)

[(0,2),(2,3),(0,3)], #(0,2,3)
[(0,2),(2,4),(0,4)], #(0,2,4)

[(0,3),(3,4),(0,4)], #(0,3,4)

[(1,2),(2,3),(1,3)], #(1,2,3)
[(1,2),(2,4),(1,4)], #(1,2,4)
[(1,3),(3,4),(1,4)], #(1,3,4)

[(2,3),(3,4),(2,4)]] #(2,3,4)
    



    list_of_volumes = [
[(0,1,2),(0,1,3),(0,2,3),(1,2,3)], #no 4
[(0,1,2),(0,1,4),(0,2,4),(1,2,4)], #no 3
[(0,1,3),(0,1,4),(0,3,4),(1,3,4)], #no 2
[(0,2,3),(0,2,4),(0,3,4),(2,3,4)], #no 1
[(1,2,3),(1,2,4),(1,3,4),(2,3,4)]  #no 0
]

    
    list_of_hypervolumes = [
[(0,1,2,3),(0,1,2,4),(0,1,3,4),(0,2,3,4),(1,2,3,4)]]
    
    return tiling4_polytope(dictionary_of_vertices,list_of_edges,list_of_faces,list_of_volumes,list_of_hypervolumes)

def hexadecahedroid():
    dictionary_of_vertices = {
(0,):Vector4(1.0,0.0,0.0,0.0),(1,):Vector4(0.0,1.0,0.0,0.0),(2,):Vector4(0.0,0.0,1.0,0.0),(3,):Vector4(0.0,0.0,0.0,1.0),
(4,):Vector4(-1.0,0.0,0.0,0.0),(5,):Vector4(0.0,-1.0,0.0,0.0),(6,):Vector4(0.0,0.0,-1.0,0.0),(7,):Vector4(0.0,0.0,0.0,-1.0)}
    
    list_of_edges = [
[(0,),(1,)],[(0,),(2,)],[(0,),(3,)],[(0,),(5,)],[(0,),(6,)],[(0,),(7,)], ######

[(1,),(2,)],[(1,),(3,)],[(1,),(4,)],[(1,),(6,)],[(1,),(7,)], #####

[(2,),(3,)],[(2,),(4,)],[(2,),(5,)],[(2,),(7,)],####

[(3,),(4,)],[(3,),(5,)],[(3,),(6,)],###

[(4,),(5,)],[(4,),(6,)],[(4,),(7,)],###

[(5,),(6,)],[(5,),(7,)],##

[(6,),(7,)] ]#
    
    



    list_of_faces = [
#not 0,1,4,5
[(0,1),(1,2),(0,2)], #(0,1,2)
[(0,1),(1,3),(0,3)], #(0,1,3)
[(0,1),(1,6),(0,6)], #(0,1,6)
[(0,1),(1,7),(0,7)], #(0,1,7)

#not 0,1,2,4,6
[(0,2),(2,3),(0,3)], #(0,2,3)
[(0,2),(2,5),(0,5)], #(0,2,5)
[(0,2),(2,7),(0,7)], #(0,2,7)

#not 0,1,2,3,4,7

[(0,3),(3,5),(0,5)], #(0,3,5)
[(0,3),(3,6),(0,6)], #(0,3,6)


#not 0,1,2,3,4,5
[(0,5),(5,6),(0,6)], #(0,5,6)
[(0,5),(5,7),(0,7)], #(0,5,7)

#not 0,1,2,3,4,5,6
[(0,6),(6,7),(0,7)], #(0,6,7)

#not 0,1,2,5,6
[(1,2),(2,3),(1,3)], #(1,2,3)
[(1,2),(2,4),(1,4)], #(1,2,4)
[(1,2),(2,7),(1,7)], #(1,2,7)

#not 0,1,2,3,5,7
[(1,3),(3,4),(1,4)], #(1,3,4)
[(1,3),(3,6),(1,6)], #(1,3,6)

#not 0,1,2,3,4,5
[(1,4),(4,6),(6,1)], #(1,4,6)
[(1,4),(4,7),(7,1)], #(1,4,7)

#not 0,1,2,3,4,5,6
[(1,6),(6,7),(1,7)], #(1,6,7)

#not 0,1,2,3,6,7
[(2,3),(3,4),(4,2)], #(2,3,4)
[(2,3),(3,5),(5,2)], #(2,3,5)

#not 0,1,2,3,4,6,
[(2,4),(4,5),(4,5)], #(2,4,5)
[(2,4),(4,7),(4,7)], #(2,4,7)

#not 0,1,2,3,4,5,6,
[(2,4),(4,7),(4,7)], #(2,4,7)
[(2,5),(5,7),(7,2)], #(2,5,7)
#not 0,1,2,4,3,7
[(3,4),(4,5),(5,3)], #(3,4,5)
[(3,4),(4,6),(6,3)], #(3,4,6)

#not 0,1,2,3,4,5,7
[(3,5),(5,6),(6,3)], #(3,5,6)

#not 0,1,2,3,4,5,
[(4,5),(5,6),(6,4)], #(4,5,6)
[(4,5),(5,7),(7,4)], #(4,5,7)

#not 0,1,2,3,4,5,6
[(4,6),(6,7),(7,4)], #(4,6,7)

#not 0,1,2,3,4,5,6
[(5,6),(6,7),(7,5)]] #(5,6,7)





    list_of_volumes = [
#not 0,1,2,4,5,6
[(0,1,2),(0,1,3),(0,2,3),(1,2,3)],#(0,1,2,3)
[(0,1,2),(0,1,7),(0,2,7),(1,2,7)],#(0,1,2,7)

#not 0,1,2,3,4,5,7
[(0,1,3),(0,1,6),(0,3,6),(1,3,6)],#(0,1,3,6)

#not 0,1,2,3,4,5,
[(0,1,6),(0,1,7),(0,6,7),(1,6,7)],#(0,1,6,7)

#not 0,1,2,3,4,6,7
[(0,2,3),(0,2,5),(0,3,5),(2,3,5)],#(0,2,3,5)

#not 0,1,2,4,5,6
[(0,2,5),(0,2,7),(0,5,7),(2,5,7)],#(0,2,5,7)


#not 0,1,2,3,5,7
[(0,3,5),(0,3,6),(0,5,6),(3,5,6)],#(0,3,5,6)

#not 0,1,2,3,4
[(0,5,6),(0,5,7),(0,6,7),(5,6,7)],#(0,5,6,7)


#not 0,1,2,3,5,6,7
[(1,2,3),(1,2,4),(1,3,4),(2,3,4)],#(1,2,3,4)

#not 0,1,2,3,4,5,6
[(1,2,4),(1,2,7),(1,4,7),(2,4,7)],#(1,2,4,7)

#not 0,1,2,3,4,5,7
[(1,3,4),(1,3,6),(1,4,6),(3,4,6)],#(1,3,4,6)

#not 0,1,2,3,4,5
[(1,4,6),(1,4,7),(1,6,7),(4,6,7)],#(1,4,6,7)


#not 0,1,2,3,4,6,7
[(2,3,4),(2,3,5),(2,4,5),(3,4,5)],#(2,3,4,5)

#not 0,1,2,3,4,5,6
[(2,4,5),(2,4,7),(2,5,7),(4,5,7)],#(2,4,5,7)

#not 0,1,2,3,4,5,7
[(3,4,5),(3,4,6),(3,5,6),(4,5,6)],#(3,4,5,6)

#not 0,1,2,3,4,5,6
[(4,5,6),(4,5,7),(4,6,7),(5,6,7)]#(4,5,6,7)

]

    
    list_of_hypervolumes = [
[(0,1,2,3),(0,1,2,7),(0,1,3,6),(0,1,6,7),(0,2,3,5),(0,2,5,7),(0,3,5,6),(0,5,6,7),(1,2,3,4),(1,2,4,7),
 (1,3,4,6),(1,4,6,7),(2,3,4,5),(2,4,5,7),(3,4,5,6),(4,5,6,7)]]
    
    return tiling4_polytope(dictionary_of_vertices,list_of_edges,list_of_faces,list_of_volumes,list_of_hypervolumes)
