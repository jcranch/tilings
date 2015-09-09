from common import cycle
from tiling3_matplotlib import default_intersection_colours

import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np
import os

def tiling2_s_flattened_subplot(tiling2_s, figure = False, number_of_rows = 1,number_of_columns = 1,position_code = 1, colours = default_intersection_colours,
                                tiling2_edge_colours = ['black'],
                                tiling2_limits = False, save_name = 'tiling2_image', folder = 'demos/tiling2',
                               save_on = True, tiling2_alpha = 0.8):
    '''
    This function is used to create 2D subplots for tiling2 objects.
    
    Number of rows and number of columns determines how the figure is subdivided into equal areas
    and the position code decides which area the subplot is plotted in. 
    
    To plot in the area in the i^{th} row and j^{th} the position code should be 
    j + (i-1)*j . 
    
    For example to plot in the top right quarter of a pictre we use 
    number_of_rows = 2, number_of_columns = 2, position_code = 1.
    '''
    

    if figure == False :
        figure = plt.figure()
        
    if tiling2_limits == False:
        bound = 0
        for tiling_2 in tiling2_s:
            if tiling_2.vertices:
                contender = max([abs(tiling_2.maxx()), abs(tiling_2.minx()),
                abs(tiling_2.miny()), abs(tiling_2.maxy())])
                if contender > bound:
                    bound = contender
                
        tiling2_limits = [[-bound-1,bound+1]]*2
    axis = plt.subplot(number_of_rows, number_of_columns,position_code, xlim = tiling2_limits[0], ylim = tiling2_limits[1], aspect='equal', frameon = False)
    axis.get_xaxis().set_visible(False)
    axis.get_yaxis().set_visible(False)
    patches = []
    grand_n = 0
    for (k,tiling2) in enumerate(tiling2_s):
        for (n,face) in enumerate(tiling2.faces):
            patches.append(axis.add_patch(plt.Polygon(0 * np.array([(v.x, v.y) for v in cycle(face)]),
            facecolor = colours[(len(face)-3)%len(colours)], edgecolor = tiling2_edge_colours[k%len(tiling2_edge_colours)] , ec='k', alpha = tiling2_alpha)))
            patches[grand_n+n].set_xy(np.array([(v.x, v.y) for v in cycle(face)]))
        grand_n += 1
    if save_on:
        folder_name = os.path.join(folder)
        if not os.path.exists(folder_name):
            os.makedirs(folder_name) 
        figure.savefig(folder+'/'+str(save_name)+'.png')         
    return axis
