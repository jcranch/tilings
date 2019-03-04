from matrix3 import rotate_x, rotate_y,rotate_z, random_special_orthogonal
from vector3 import Vector3
from restrict32 import restrict32
from common import cycle
from tiling3 import Tiling3

from random import random

def random_intersection(tiling3):
    '''
    Takes the original tiling3 object randomly rotates it about the origin.
    Then it randomly translates the tiling3 such that it still intersects the plane z = 0.
    '''
    rotated_tiling3 = tiling3.deform(random_special_orthogonal())
    bound = max([abs(tiling3.minx()),abs(tiling3.maxx()),
                 abs(tiling3.miny()),abs(tiling3.maxy()),
                 abs(tiling3.minz()),abs(tiling3.maxz())])
    translation = Vector3(0,0,(2*random() - 1)*bound)
    random_intersection = rotated_tiling3.translate(translation)
    return random_intersection


def montecarlo_tiling3_cross_section_density(tiling3_s ,polygon_side_length_only_on = True):
    '''
    tiling3_s should be a list of tiling3 objects we wish to know the distribution of intersection
    Returns the monte-carlo distribution of 2d cross-section of Tiling3 objects under certain tranformations.
    polygon_sides_only_on determines whether or not to display how the n-gon was formed or the specific faces 
    the edge is formed upon.
    '''
    raw_n_gon_count_results = {}
    hits = 0.0
    for tiling3 in tiling3_s:
        restrict = restrict32(tiling3)
        intersect_lines = frozenset(restrict.edges[e] for f in restrict.faces for e in f)
        if polygon_side_length_only_on == True and intersect_lines:
            intersect_lines = str(len(intersect_lines))+'-gons'
        try:
            raw_n_gon_count_results[(intersect_lines)] += 1
            hits += 1
        except:
            if intersect_lines:
                raw_n_gon_count_results[(intersect_lines)] = 0.0
                hits += 1
    density_dictionary = dict([(intersect_lines,raw_n_gon_count_results[intersect_lines]/hits) for intersect_lines in raw_n_gon_count_results])
    return density_dictionary



