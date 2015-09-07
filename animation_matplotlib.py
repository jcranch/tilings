from polygon_count import *
from tiling3_matplotlib import tiling3_s_3d_subplot
from tiling2_matplotlib import tiling2_s_flattened_subplot
from data_line_matplotlib import line_plot_2d
from simultaneous_plot import simultaneous_plot 
import os
import matplotlib.pyplot as plt

def restriction_full_animation(list_of_tiling3_s, face_count_tiling = 'tiling3' ,
             common_colours = default_intersection_colours,
             save_name = 'tiling_image', folder = 'demos/tiling', save_on = True, figure_size = (20,10),
             
             tiling3_s_on = True, tiling3_position_code = 222,  
             plane_z0_on = False, restrict32_intersection_on = False, tiling3_edges_on = True,
             tiling3_faces_on = True,tiling3_edge_colours = ['black'],
             tiling3_axis_limit = False, elevation = 30, azumith = 30,  
             plane_z0_alpha = 0.2, restrict32_alpha = 0.8, tiling3_faces_alpha = 0.8, tiling3_edges_alpha = 0.8,
             
             tiling2_s_on = True, tiling2_position_code = 221,tiling2_edge_colours = ['black'], tiling2_limits = False,tiling2_alpha = 0.8,
             
             data_lines_on  = True, x_s = False, data_position_code = 313, 
             legend_on = True, marker_style = 'polygon',
             data_lines_x_label = 'Iteration', data_lines_y_label = '2D Cross-section Polygon Count',
             index_start = False , index_end = False):
    '''
    
    This function will take in list_of_tiling3_s and will make a simultaneous plot for 
    each tiling3 with the tiling2 being the retrict32(tiling3) and the data_lines either being the number of faces 
    on the tiling3 or the restrict32(tiling3) (determined by assigning the variable face_count_tiling = 'tiling2' or
    face_count_tiling = 'tiling3'.
    
    list_of_tiling3_s should be a list such that the i^{th} element is a single tiling3 object that you wish to
    display on the i^{th} frame. 
    
    This function should be used to make animations that contain tiling3 objects as well as data lines and restrict32 projections.
    
    For animations that just require a tiling3 image it is reccomended that the user uses tiling3_s_animation function instead.
    '''
    list_of_tiling2_s = [0]*len(list_of_tiling3_s)
    
    if tiling2_s_on or face_count_tiling == 'tiling2':
        list_of_tiling2_s = []
        for tiling3 in list_of_tiling3_s:
            list_of_tiling2_s.append(restrict32(tiling3))
    
    dictionary_of_dictionary_of_y_s = dict([(i,0) for i in range(len(list_of_tiling3_s))])
    for i in range(len(list_of_tiling3_s)):
        if data_lines_on:
            if face_count_tiling == 'tiling2':
                dictionary_of_dictionary_of_y_s[i] = list_of_dictionary_of_y_s_creater(list_of_tiling2_s)
            elif face_count_tiling == 'tiling3':
                dictionary_of_dictionary_of_y_s[i] = list_of_dictionary_of_y_s_creater(list_of_tiling3_s)
        simultaneous_plot([list_of_tiling3_s[i]],[list_of_tiling2_s[i]],dictionary_of_dictionary_of_y_s[i], common_colours ,
             save_name + '_' + str(i) , folder , save_on , figure_size ,
             
             tiling3_s_on, tiling3_position_code,  
             plane_z0_on, restrict32_intersection_on , tiling3_edges_on ,
             tiling3_faces_on ,tiling3_edge_colours,
             tiling3_axis_limit , elevation , azumith ,  
             plane_z0_alpha , restrict32_alpha , tiling3_faces_alpha , tiling3_edges_alpha ,
             
             tiling2_s_on , tiling2_position_code ,tiling2_edge_colours, tiling2_limits ,tiling2_alpha ,
             
             data_lines_on  , x_s , data_position_code , 
             legend_on , marker_style ,
             data_lines_x_label , data_lines_y_label ,
             index_start = 0 , index_end = i + 1)
    return None


def tiling3_s_animation(list_of_tiling3_s, figure = False, position_code = 111, colours = default_intersection_colours, 
                      plane_z0_on = False, restrict32_intersection_on = False, tiling3_edges_on = True,
                      tiling3_faces_on = True,tiling3_edge_colours = ['black'],
                      axis_limit = False, elevation = 30, azumith = 30, 
                      save_name = 'tiling3_image', folder = 'demos/tiling3animation', save_on = True, 
                      plane_z0_alpha = 0.2, restrict32_alpha = 0.8, tiling3_faces_alpha = 0.8, tiling3_edges_alpha = 0.8):
    '''
    This function takes a list of list of tiling3 objects, list_of_tiling3_s, and creates a tiling3_s_3d_subplot
    for each tiling3_s. 
    
    This can be used to make quick animations of tiling3 objects.
    
    '''
    for (j,tiling3_s) in enumerate(list_of_tiling3_s):
        tiling3_s_3d_subplot(tiling3_s, figure, position_code, colours, 
                      plane_z0_on, restrict32_intersection_on, tiling3_edges_on,
                      tiling3_faces_on,tiling3_edge_colours,
                      axis_limit, elevation, azumith, 
                      save_name +str(j), folder, save_on, 
                      plane_z0_alpha, restrict32_alpha, tiling3_faces_alpha , tiling3_edges_alpha)
    return None
