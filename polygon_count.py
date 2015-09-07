from tiling3_matplotlib import default_intersection_colours

def default_line_plot_2d_dictionary_of_y_s_maker(y_s, n, colours = default_intersection_colours):
    '''
    An auxillary function for making data lines for plots.
    Prepares dictionaries for polygon_count_info.
    '''
    return {'name':str(n)+'-gon', 'data':y_s, 'colour' : colours[(n-3)%len(colours)], 'alpha' : 0.9, 'n':n}



def polygon_count_info(tiling2_s):
    '''
    An auxillary function for making data lines for plots.
    prepares produce_polygon_count_lines
    '''
    raw_n_gon_count_results = []
    tiling2_faces = []
    tiling3_edges = []
    for (j,tiling2) in enumerate(tiling2_s):
        raw_n_gon_count_results.append(tiling2.face_count_information())
    distinct_n_gons_found = []
    for dictionary_of_n_gons in raw_n_gon_count_results:
        for n_gon in dictionary_of_n_gons:
            if n_gon not in distinct_n_gons_found:
                distinct_n_gons_found.append(n_gon)
    data_lines = dict([(n_gon,[]) for n_gon in distinct_n_gons_found])

    max_number_of_faces = 0.0
    for j in range(len(tiling2_s)):
        for n_gon in distinct_n_gons_found:
            if n_gon in raw_n_gon_count_results[j]:
                data_lines[n_gon].append(raw_n_gon_count_results[j][n_gon])
                if raw_n_gon_count_results[j][n_gon] > max_number_of_faces:
                    max_number_of_faces = raw_n_gon_count_results[j][n_gon]
            else :
                data_lines[n_gon].append(0.0)
    return data_lines

def produce_polygon_count_lines(tiling_2_s):
    return [default_line_plot_2d_dictionary_of_y_s_maker(j,i) for (i,j) in polygon_count_info(tiling2_s).iteritems()]
