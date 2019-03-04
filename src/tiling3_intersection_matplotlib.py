from math import pi, floor, cos
from random import random
import Image
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from matrix3 import rotate_x,rotate_z
from vector3 import Vector3
from restrict32 import restrict32
from styling import default_intersection_colours


def distribution_plot(polyhedron,iterations = 100000, colours = default_intersection_colours, plot_on = True):
    bound = max(vertex.norm() for vertex in polyhedron.vertices) # Takes length from origin.
    cases = {}
    dictionary_of_tallies = {}
    for iteration in range(iterations):
        theta_x = random()*pi/2 # longitude on normal hemisphere
        theta_z = random()*2*pi # latitude
        rotation_matrix = rotate_x(theta_x)*rotate_z(theta_z)
        translation = (2*random()-1)*bound
        transformed_polyhedron = polyhedron.transform(rotation_matrix).translate(Vector3(0,0,translation))
        intersection = restrict32(transformed_polyhedron)
        case = frozenset(intersection.edges[edge] for face in intersection.faces for edge in face)
        if case:
            try:
                cases[case] += [(theta_x,theta_z,translation)]
                dictionary_of_tallies[case] += 1
            except:
                cases[case] = [(theta_x,theta_z,translation)]
                dictionary_of_tallies[case] = 0.0
    if plot_on:
        figure = plt.figure()
        axis = Axes3D(figure)
        axis.set_xlabel('Longitude')
        axis.set_ylabel('Latitude')
        axis.set_zlabel('Displacement')
        total_length = 0
        for (count, case) in enumerate(cases):
            x_s = []
            y_s = []
            z_s = []
            for (theta_x,theta_z,translation) in cases[case] :
                x_s += [theta_x]
                y_s += [theta_z]
                z_s += [translation]
            axis.plot(x_s, y_s, z_s, ',', color = colours[count%len(colours)], label = str(case) )
            total_length += len(x_s)
    plt.show()
    dictionary_of_distributions = dict([(case,(dictionary_of_tallies[case]/total_length,str(colours[count%len(colours)])))\
                                        for (count,case) in enumerate(cases)])

    return dictionary_of_distributions
