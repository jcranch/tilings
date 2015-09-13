from polygon_count import *
from tiling3_matplotlib import tiling3_s_3d_subplot
from tiling2_matplotlib import tiling2_s_flattened_subplot
from data_line_matplotlib import line_plot_2d

import os
import matplotlib.pyplot as plt

def simultaneous_plot(tiling3_s, tiling2_s, list_of_dictionary_of_y_s,
             common_colours = default_intersection_colours,
             save_name = 'tiling_image', folder = 'demos/tiling', save_on = True, figure_size = (20,10),

             tiling3_s_on = True,
             tiling3_s_number_of_rows = 2,tiling3_s_number_of_columns = 2,tiling3_s_position_code = 1,
             plane_z0_on = False, restrict32_intersection_on = False, tiling3_edges_on = True,
             tiling3_faces_on = True,tiling3_edge_colours = ['black'],
             tiling3_axis_limit = False, elevation = 30, azimuth = 30,
             plane_z0_alpha = 0.2, restrict32_alpha = 0.8, tiling3_faces_alpha = 0.8, tiling3_edges_alpha = 0.8,

             tiling2_s_on = True,
             tiling2_s_number_of_rows = 2,tiling2_s_number_of_columns = 2,tiling2_s_position_code = 2,
             tiling2_edge_colours = ['black'], tiling2_limits = False,tiling2_alpha = 0.8,

             data_lines_on  = True, x_s = False,
             data_number_of_rows = 2,data_number_of_columns = 1,data_position_code = 2,
             legend_on = True, marker_style = 'polygon',
             data_lines_x_label = 'Iteration', data_lines_y_label = '2D Cross-section Polygon Count',
             index_start = False , index_end = False):
    '''
    This function can simultaneously plot tiling3_s_3d_subplot, tiling2_s_3d_subplot and line_plot_2d.

    Whether or not each subplot is plotted or not is determined by
    -tiling3_s_on = True or False,
    -tiling2_s_on = True or False,
    -data_lines_on = True or False,

    The position of each subplot is determined by a 3-digit decimal code where the
    - 1st digit determines the number of rows considered
    - 2nd digit determines the number of columns considered
    - 3rd digit determines the position of subplot where the position on row_i, col_j is denoted by digit i + j.

    (For example, for a subplot to placed in the top-left corner of a figure we use the code 222.)

    This an auxillary function for restriction animations with stats.
    '''

    common_figure = plt.figure(figsize = figure_size)


    if tiling2_s_on:
        tiling2_s_flattened_subplot(tiling2_s,common_figure,
        tiling2_s_number_of_rows, tiling2_s_number_of_columns, tiling2_s_position_code,
        common_colours,tiling2_edge_colours,
                                    tiling2_limits, 'not_required', 'not_required', False, tiling2_alpha)
    if tiling3_s_on:
        tiling3_s_3d_subplot(tiling3_s, common_figure,
        tiling3_s_number_of_rows, tiling3_s_number_of_columns, tiling3_s_position_code , common_colours,
                          plane_z0_on, restrict32_intersection_on,
                          tiling3_edges_on,tiling3_faces_on,tiling3_edge_colours,
                          tiling3_axis_limit, elevation, azimuth,
                          'not_required','not_required', False,
                          plane_z0_alpha, restrict32_alpha,
                          tiling3_faces_alpha,tiling3_edges_alpha)

    if data_lines_on:
        line_plot_2d(list_of_dictionary_of_y_s, x_s,
        data_number_of_rows, data_number_of_columns, data_position_code,common_figure,
                     legend_on, marker_style,
                     data_lines_x_label, data_lines_y_label, index_start , index_end,
                     save_on = False)

    if save_on:
        folder_name = os.path.join(folder)
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        common_figure.savefig(folder+'/'+str(save_name)+'.png')
    return common_figure
