from matrix3 import random_special_orthogonal
from restrict32 import restrict32
from vector3 import Vector3
from tiling3_matplotlib import default_intersection_colours

from random import random
import matplotlib.pyplot as plt

def random_dissection_distribution(polyhedron, iterations = 1000,plot_on = True, colours = default_intersection_colours):
    case_tally = {}
    total_hits = 0
    bound = max(v.norm() for v in polyhedron.vertices)
    min_translation = 0
    max_translation = 0
    translations = []
    for i in xrange(iterations):
        translation = (2*random()-1)*bound
        translations.append(translation)
        if translation > max_translation:
            max_translation = translation
        if translation < min_translation:
            min_translation = translation
    for i in xrange(iterations):
        rotation_matrix = random_special_orthogonal()
        transformed_polyhedron = polyhedron.transform(rotation_matrix).translate(Vector3(0,0,translations[i]))
        restriction = restrict32(transformed_polyhedron)
        intersection = frozenset(restriction.edges[e] for f in restriction.faces for e in f)
        v3 = rotation_matrix.column(3)
        if v3[3] < 0 :
            v3 = - v3
        try :
            case_tally[intersection].append(v3*(1+translation-min_translation))
            total_hits += 1
        except :
            if intersection:
                case_tally[intersection] = [v3*(1+translation-min_translation)]
                total_hits += 1
    
    density_of_cases = dict([(k,(float(len(case_tally[k]))/total_hits,colours[count%len(colours)])) for (count,k) in enumerate(case_tally)])
    
    if plot_on == True:
        figure = plt.figure()
        axis = figure.add_subplot(111,projection = '3d')
        plt.gca().set_aspect('equal', adjustable='box')
        for (count,case) in enumerate(case_tally):
            for normal in case_tally[case]:
                axis.plot([normal[1]],[normal[2]],[normal[3]], 'o', color = colours[count%len(colours)])
        plt.show()
    return density_of_cases
