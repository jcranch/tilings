from periodic_tiling3 import cubic_tiling3
from matrix3 import rotate_x, rotate_y,rotate_z, random_special_orthogonal
from vector3 import Vector3
from restrict32 import restrict32
from common import cycle
from tiling3 import Tiling3



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

#Seems to tend to {4: 0.65,6:0.35}
montecarlo_so3(iterations,tiling3 = unit_cube, transformation_function = deform_matrix)
