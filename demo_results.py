from monte_carlo_so3 import random_intersection, montecarlo_tiling3_cross_section_density
from tiling3_polyhedron import regular_polytopes_3d 


'''
Finds the distribution of random cross-section for the Platonic Solids.
'''

for polytope in regular_polytopes_3d:
    print tiling3_polyhedron, montecarlo_tiling3_cross_section_density(
    [random_intersection(regular_polytopes_3d[tiling3_polyhedron]) for i in range(100000)])
    

