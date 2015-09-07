from tiling3_matplotlib import default_intersection_colours
from vector3 import Vector3, random_norm1
from matrix3 import Matrix3, rotation_matrix_producer

import numpy as np
import matplotlib.pyplot as plt

def polyhedron_fixed_plane_exact_distribution(polyhedron, plane_vector_1, plane_vector_2, number_of_planes = 1000,
                                              colours = default_intersection_colours, epsilon = 0.00001, construction_lines_on = True,
                                              plot_on = True):
    '''
    This function takes a polyhedron and intersects it with a family of parallel planes
    specified by the user and intersects the planes with the polyhedron. The function 
    then calculates the proportion of which combination of faces were intersected and 
    has an optional matplotlib display to demonstrate this.
    '''
    bound = max(v.norm() for v in polyhedron.vertices)
    if plot_on == True:
        figure = tiling3_s_3d_subplot([polyhedron])  
        
    normal_vector = normal_vector_creator(plane_vector_1, plane_vector_2)
    
    dictionary_of_vertices = {}
    list_of_intersections = {}
    list_of_vertices = []
    
    # Solve the points of intersection using matrices in numpy.
    for (count,vertex) in enumerate(polyhedron.vertices):
        a_11 = plane_vector_1[1]
        a_21 = plane_vector_1[2]
        a_31 = plane_vector_1[3]
        
        a_12 = plane_vector_2[1]
        a_22 = plane_vector_2[2]
        a_32 = plane_vector_2[3]  
        
        a_13 = -normal_vector[1]
        a_23 = -normal_vector[2]
        a_33 = -normal_vector[3]
        
        co_efficients_matrix = np.array([[a_11,a_12,a_13],[a_21,a_22,a_23],[a_31,a_32,a_33]])
        constants_vector = np.array([-vertex[1],-vertex[2],-vertex[3]])
        intersection_point = np.linalg.solve(co_efficients_matrix, constants_vector)
        
        list_of_intersections[intersection_point[2]] = \
        Vector3(intersection_point[2]*normal_vector[1], intersection_point[2]*normal_vector[2], intersection_point[2]*normal_vector[3])
        
        list_of_vertices += [intersection_point[2]]
        
        dictionary_of_vertices[intersection_point[2]] = [vertex]
        if plot_on == True:
            if construction_lines_on == True:
                plt.plot([(vertex[1]+i/100.0*plane_vector_1[1]+j/100.0*plane_vector_2[1]) for i in range(-10,10) for j in range(-10,10)],
                         [(vertex[2]+i/100.0*plane_vector_1[2]+j/100.0*plane_vector_2[2]) for i in range(-10,10) for j in range(-10,10)],
                         [(vertex[3]+i/100.0*plane_vector_1[3]+j/100.0*plane_vector_2[3]) for i in range(-10,10) for j in range(-10,10)],
                         '-',color = colours[count%len(colours)])

                plt.plot([intersection_point[2]*normal_vector[1]],[intersection_point[2]*normal_vector[2]],
                         [intersection_point[2]*normal_vector[3]],'o', alpha = 0.7, color = colours[count%len(colours)])

    if plot_on == True:
        if construction_lines_on == True:
            plt.plot([normal_vector[1]*i/100.0 for i in range(-200,200)],[normal_vector[2]*i/100.0 for i in range(-200,200)],
                     [normal_vector[3]*i/100.0 for i in range(-200,200)],'--', color = 'black', lw = 2, alpha = 0.8)
    
    list_of_vertices = sorted(list_of_vertices)
    total_length = list_of_intersections[list_of_vertices[0]].distance(list_of_intersections[list_of_vertices[::-1][0]])
    
    dictionary_of_distributions = {}
    
    for (count) in range(len(list_of_vertices)-1):
        dictionary_of_distributions[(list_of_intersections[list_of_vertices[count]],list_of_intersections[list_of_vertices[count+1]])]=\
        list_of_intersections[list_of_vertices[count]].distance(list_of_intersections[list_of_vertices[count+1]])/total_length
    intersection_keys = {}
    
    # Now we find out where the planes spanned at the mid points of where the planes intersects normal vectors
    # intersect the faces of the polyhedron.
    for key in dictionary_of_distributions:
        # We do not consider vertices are epsilon apart as they are probably duplicates due to symetry.
        if key[0].distance(key[1]) >epsilon:
            mid_point = (key[0]+key[1])/2.0
            n = 1.0
            if mid_point[3] < 0.0:
                n = 0.0
            translation = Vector3(0,0,(-1)**n*mid_point.norm())
            rotation_matrix = rotation_matrix_producer(normal_vector)
            restrict = restrict32(polyhedron.transform(rotation_matrix).translate(translation))
            intersect_lines = frozenset(restrict.edges[e] for f in restrict.faces for e in f)
            intersection_keys[(intersect_lines)] = (dictionary_of_distributions[key])

    return intersection_keys
