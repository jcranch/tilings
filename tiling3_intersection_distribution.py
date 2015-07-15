
def tiling3_intersection_distribution(polyhedron = tetrahedron(),iterations = 100000, colours = default_intersection_colours):
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
    total_length = sum([dictionary_of_tallies[case] for case in cases])
    dictionary_of_distributions = dict([(case,(dictionary_of_tallies[case]/total_length,str(colours[count%len(colours)])))\
                                        for (count,case) in enumerate(cases)])
    
    return dictionary_of_distributions
    
    
