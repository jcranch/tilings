import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np
from common import cycle
from tiling3_matplotlib import default_intersection_colours

import os

def tiling2_s_flattened_subplot(tiling2_s, figure = False, position_code = 111, colours = default_intersection_colours,
                                xlimits = [-5,5], ylimits = [-5,5], save_name = 'tiling2_image', folder = 'demos/tiling2',
                               save_on = True):
    if figure == False :
        figure = plt.figure()
    folder_name = os.path.join(folder, save_name+"_png")
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    axis = plt.subplot(position_code, xlim = xlimits, ylim = ylimits, aspect='equal', frameon = False)
    axis.get_xaxis().set_visible(False)
    axis.get_yaxis().set_visible(False)
    patches = []
    grand_n = 0
    for tiling2 in tiling2_s:
        for (n,face) in enumerate(tiling2.faces):
            patches.append(axis.add_patch(plt.Polygon(0 * np.array([(v.x, v.y) for v in cycle(face)]),
            facecolor = colours[(len(face)-3)%len(colours)] , ec='k', alpha = 0.6)))
            patches[grand_n+n].set_xy(np.array([(v.x, v.y) for v in cycle(face)]))
        grand_n += 1
    if save_on == True:
        figure.savefig(os.path.join(folder_name, str(save_name)))         
    return axis
