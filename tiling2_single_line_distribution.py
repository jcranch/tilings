from tiling2_matplotlib import plot_matplotlib
from math import  tan
from vector2 import Vector2
from restrict21 import restrict21
from matrix2 import rotation
import matplotlib.pyplot as plt



def polygon_fixed_line_exact_distribution(polygon,line_angle, plot_on = True):
    '''
    This function aims to calculate the exact distribution
    of each qualitative case that can occur by intersecting
    a given polygon with a family of lines with the same
    gradient.
    '''
    bound = max(v.norm() for v in polygon.vertices)
    if plot_on == True:
        plot_matplotlib(polygon)
    x_s  = np.linspace(-bound-1,bound+1,1000)
    list_of_y_s = []
    list_of_normal_intersections = []
    # We construct a line with the given gradient that passes through each vertex.
    # We then intersect this line with the normal line that passes through the origin
    # and use this to measure the length between points of intersection.
    for vertex in polygon.vertices:
        y_s  = tan(line_angle)*(x_s - vertex[1])+vertex[2]
        list_of_y_s += [y_s]
        normal_intersection_x = (tan(line_angle)**2*vertex[1]- tan(line_angle)*vertex[2])/(1 + tan(line_angle)**2)
        normal_intersection_y = -1.0/tan(line_angle)*normal_intersection_x
        y_normals = -1/tan(line_angle)*(x_s)
        list_of_normal_intersections += [((normal_intersection_x,normal_intersection_y),vertex)]
        if plot_on == True:
            plt.plot(normal_intersection_x,normal_intersection_y,color = 'black',marker = 'o')
            plt.plot(x_s,y_s, '--', color = 'black', lw = 2, alpha = 0.5)
            plt.plot(x_s,y_normals,'--', color = 'grey', lw = 2, alpha = 0.5)




    list_of_normal_intersections = sorted(list_of_normal_intersections)

    total_length = ((list_of_normal_intersections[0][0][0] - list_of_normal_intersections[::-1][0][0][0])**2 +\
    (list_of_normal_intersections[0][0][1] - list_of_normal_intersections[::-1][0][0][1])**2)**0.5

    #We now find the ratios.
    dictionary_of_intersections_actual = {}
    for index in range(len(list_of_normal_intersections)-1):
        dictionary_of_intersections_actual[list_of_normal_intersections[index],list_of_normal_intersections[index+1]] = \
        ((list_of_normal_intersections[index][0][0] - list_of_normal_intersections[index+1][0][0])**2 +\
    (list_of_normal_intersections[index][0][1] - list_of_normal_intersections[index+1][0][1])**2)**0.5/total_length

    #We now make keys that correspond to which edges have been intersected.
    new_dictionary_of_results = {}
    for key in dictionary_of_intersections_actual:
        n = 1
        displacement = (Vector2(key[0][0][0],key[0][0][1])+Vector2(key[1][0][0],key[1][0][1]))/2.0
        if displacement[2] < 0:
            n = 0
        normalised_displacement = Vector2(0, (-1)**n *displacement.norm())

        if plot_on == True:
            plt.plot([displacement[1]],[displacement[2]],'o',color = 'grey')
        rotation_matrix = rotation(line_angle)
        transformed_polygon = polygon.transform(rotation_matrix).translate(normalised_displacement)
        restrict = restrict21(transformed_polygon)
        intersect_lines = frozenset(restrict.vertices[v] for e in restrict.edges for v in e)
        new_dictionary_of_results[intersect_lines] = dictionary_of_intersections_actual[key]
    if plot_on == True:
        plt.show()
    return new_dictionary_of_results
