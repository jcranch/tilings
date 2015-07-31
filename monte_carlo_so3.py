from periodic_tiling3 import cubic_tiling3
from matrix3 import rotate_x, rotate_y,rotate_z, random_special_orthogonal
from vector3 import Vector3
from restrict32 import restrict32
from common import cycle
from tiling3 import Tiling3

# Conceptually This function takes a tiling and rotates it using a uniformly, randomly selected rotation matrix in SO3
# then counts polygons in the intersection of z = 0. This is designed to be repeated for many iterations.

def montecarlo_so3(iterations, tiling3, transformation_function ):
    # Take the tiling3, transform it wrt i and count the polygons on restrict32.
    raw_n_gon_count_results = []
    for i in range(iterations):
        transforming_3d_tiling = transformation_function(tiling3,i)
        transforming_2d_intersection = restrict32(transforming_3d_tiling).clip(-20,20,-20,20)
        raw_n_gon_count_results += [transforming_2d_intersection.face_count_information()]
    # Determine the unique n-gons that were found in the intersection.
    distinct_n_gons_found = []
    for dictionary_of_n_gons in raw_n_gon_count_results:
        for n_gon in dictionary_of_n_gons:
            if n_gon not in distinct_n_gons_found:
                distinct_n_gons_found += [n_gon]
    # Count how many of each n-gon were found overall.
    n_gon_tally = dict([(n_gon,0) for n_gon in distinct_n_gons_found])
    total_n_gons = 0.0
    max_number_of_faces = 0.0
    for i in range(iterations):
        for n_gon in distinct_n_gons_found:
            if n_gon in raw_n_gon_count_results[i]:
                n_gon_tally[n_gon] += raw_n_gon_count_results[i][n_gon]
                total_n_gons += raw_n_gon_count_results[i][n_gon]
                if raw_n_gon_count_results[i][n_gon] > max_number_of_faces:
                    max_number_of_faces = raw_n_gon_count_results[i][n_gon]
    # Return the fraction of each.
    n_gon_distribution = dict([(n_gon,n_gon_tally[n_gon]/total_n_gons) for n_gon in distinct_n_gons_found])
    return n_gon_distribution


#Example:

unit_cube = cubic_tiling3(((-0.2,1.2),(-0.2,1.2),(-0.2,1.2))).translate(Vector3(-0.50000001,-0.50000001,-0.50000001))
iterations = 1000

def produce_k_random_rotations_so3(k = iterations):
    list_of_random_so3_rotations = []
    for i in range(k):
        list_of_random_so3_rotations += [random_special_orthogonal()]
    return list_of_random_so3_rotations

def deform_matrix(tiling3, i,list_of_matrices = produce_k_random_rotations_so3()):
    return tiling3.transform(list_of_matrices[i])

#Seems to tend to something like {4: 0.65,6:0.35}.
#montecarlo_so3(iterations,tiling3 = unit_cube, transformation_function = deform_matrix)

# Conceptually this function takes a 3d tiling, rotates randomly (as described before)
# then translates it (preferably so that all the tiling is above z = 0)
# and then slowly translates it frame by frame (preferably so that  all of the tiling is below z = 0)
# whilst counting the n-gons produced with the intersection of z = 0.
# It then returns the distribution of n-gons produced this way for all of randomly rotated 3d objects.
def translation_function(tiling3,i):
    return tiling3.translate(Vector3(0,0,-i/1000.0))


def montecarlo_polygon_density(transformation_iterations=100,  tiling3 = unit_cube,\
                               transformation_function = deform_matrix,translation_function = translation_function,\
                               translation_count_safetylimit = 1000000):
    grand_list_of_distinct_n_gons = []
    grand_n_gon_tally = {}
    grand_total_n_gons = 0.0
    # Takes a tiling and rotates it.
    for i in range(transformation_iterations):
        transforming_3d_tiling = transformation_function(tiling3,i)
        # If the 'lowest' point of the tiling lies below z = 0 then reaise it so that it lies just above.
        if transforming_3d_tiling.minz() < 0:
            transforming_3d_tiling = transforming_3d_tiling.translate(Vector3(0,0,-transforming_3d_tiling.minz()+0.000000001))
        raw_n_gon_count_results = []
        # Now we begin translating the given rotated tiling (preferably so that all of it lies below z = 0).
        translation_count = 0
        translating_3d_tiling = transforming_3d_tiling
        # Translate it until 'highest' point in tiling is below z = 0 and record intersections of z = 0 along the way frame by frame.
        while translating_3d_tiling.maxz() > 0 :
            translating_3d_tiling = translation_function(transforming_3d_tiling,translation_count)
            translating_2d_intersection = restrict32(translating_3d_tiling).clip(-20,20,-20,20)
            # Record the n-gons that intercepted z = 0 this frame.
            raw_n_gon_count_results += [translating_2d_intersection.face_count_information()]
            translation_count += 1
            if  translation_count > translation_count_safetylimit:
                print "Translation count safetylimit has been surpassed."
                break
        # Find which n-gons were actually found. (I think I might be able to remove/improve this part!)
        distinct_n_gons_found = []
        for dictionary_of_n_gons in raw_n_gon_count_results:
            for n_gon in dictionary_of_n_gons:
                if n_gon not in distinct_n_gons_found:
                    distinct_n_gons_found += [n_gon]
                if n_gon not in grand_list_of_distinct_n_gons:
                    grand_list_of_distinct_n_gons += [n_gon]
        # Count how many of each n-gon were found overall.
        for k in range(translation_count):
            for n_gon in distinct_n_gons_found:
                if n_gon in raw_n_gon_count_results[k]:
                    grand_total_n_gons += raw_n_gon_count_results[k][n_gon]
                    # Add results to our overall list
                    try :
                        grand_n_gon_tally[n_gon] += raw_n_gon_count_results[k][n_gon]
                    except:
                        grand_n_gon_tally[n_gon] = raw_n_gon_count_results[k][n_gon]
    grand_n_gon_distribution = dict((n_gon,grand_n_gon_tally[n_gon]/grand_total_n_gons ) for n_gon in grand_list_of_distinct_n_gons)
    return grand_n_gon_distribution



'''
For unit cube with 10000 transformation iterations I got this :
montecarlo_polygon_density()
>>> {3: 0.2776192417448023,
 4: 0.4866707210307887,
 5: 0.18974424090942507,
 6: 0.045965796314983993}
'''
montecarlo_polygon_density()
