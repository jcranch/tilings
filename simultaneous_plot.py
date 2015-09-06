from polygon_count import *
from tiling3_matplotlib import tiling3_s_3d_subplot
from tiling2_matplotlib import tiling2_s_flattened_subplot
from data_line_matplotlib import line_plot_2d

import os
import matplotlib.pyplot as plt

def all_plot(tiling3_s, tiling2_s, list_of_dictionary_of_y_s, 
             common_colours = default_intersection_colours,
             save_name = 'tiling_image', folder = 'demos/tiling', save_on = True, figure_size = (20,10),
             
             tiling3_s_on = True, tiling3_position_code = 222,  
             plane_z0_on_ = False, restrict32_intersection_on_ = False, tiling3_edges_on_ = True,
             tiling3_faces_on_ = True,
             tiling3_axis_limit_ = [[-2,2],[-2,2],[-2,2]], elevation_ = 30, azumith_ = 30,  
             plane_z0_alpha_ = 0.2, restrict32_alpha_ = 0.8, tiling3_faces_alpha_ = 0.8, tiling3_edges_alpha_ = 0.8,
             
             tiling2_s_on = True, tiling2_position_code = 221, tiling2_xlimits = [-5,5], tiling2_ylimits = [-5,5],
             
             data_lines_on  = True, x_s = False, data_position_code = 313, figure = False,
             legend_on_ = True, marker_style_ = 'polygon',
             data_lines_x_label = 'Iteration', data_lines_y_label = '2D Cross-section Polygon Count',
             index_start_ = False , index_end_ = False):


    folder_name = os.path.join(folder, save_name+"_png")
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)    
    
    common_figure = plt.figure(figsize = figure_size)
    
    
    if tiling2_s_on:
        tiling2_s_flattened_subplot(tiling2_s, figure = common_figure, position_code = tiling2_position_code, 
                                    colours = common_colours,
                                    xlimits = tiling2_xlimits, ylimits = tiling2_ylimits, save_on = False)
    if tiling3_s_on:
        tiling3_s_3d_subplot(tiling3_s, figure = common_figure, position_code = tiling3_position_code, colours = common_colours, 
                          plane_z0_on = plane_z0_on_, restrict32_intersection_on = restrict32_intersection_on_, 
                          tiling3_edges_on = tiling3_edges_on_,
                          tiling3_faces_on = tiling3_faces_on_,
                          axis_limit = tiling3_axis_limit_, elevation = elevation_, azumith = azumith_, 
                          save_on = False, 
                          plane_z0_alpha = plane_z0_alpha_, restrict32_alpha =restrict32_alpha_, 
                          tiling3_faces_alpha = tiling3_faces_alpha_,tiling3_edges_alpha =tiling3_edges_alpha_)
    
    if data_lines_on:
        line_plot_2d(list_of_dictionary_of_y_s, x_s = False, position_code = data_position_code, figure = common_figure,
                     legend_on = legend_on_, marker_style = marker_style_,
                     x_label = data_lines_x_label, y_label = data_lines_y_label, index_start = index_start_ , index_end = index_end_, 
                     save_on = False)
    if save_on == True:
        figure.savefig(os.path.join(folder_name, str(save_name)))         
    return common_figure
    
