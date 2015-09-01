import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np
from matplotlib import animation

from common import cycle


default_colours = ['orange','lime','red','aqua','magenta','darkgreen','lightblue','gold','black','purple','blue','darkred','darkblue','lightgreen']


def describe_polygon_path(polygon):
    """
    The polygon should be specified as a list of vertices of the form
    [(a,b),(c,d)....(x,y)].
    """
    vertices = []
    for vertex in polygon:
        vertices.append(vertex)
    vertices.append(polygon[0])
    codes = [Path.MOVETO] + [Path.LINETO]*(len(polygon)-1) + [Path.CLOSEPOLY]
    return Path(vertices, codes)


def plot_matplotlib(tiling2, figure_size=8, grid_on=True,
                    ticks_on=True, colours=default_colours, alpha=0.85):

    """
    Alpha determines translucency.
    """

    figure = plt.figure()
    figure.set_size_inches(figure_size,figure_size)
    axis = figure.add_subplot(111)
    for (i,face) in enumerate(tiling2.faces):
        l = describe_polygon_path([(v.x, v.y) for v in cycle(face)])
        patch = patches.PathPatch(l, facecolor=colours[(len(face)-3)%len(colours)], lw=1.3, ec='k', alpha=alpha)
        axis.add_patch(patch)
    plt.axis('scaled')
    axis.set_xlim(tiling2.minx()-1, tiling2.maxx()+1)
    axis.set_ylim(tiling2.miny()-1, tiling2.maxy()+1)
    if grid_on == True :
        axis.grid(True)
    if ticks_on == False:
        axis.set_xticks([])
        axis.set_yticks([])
    return figure

def plot_matplotlib_multiple(tiling2_s, figure_size=8, grid_on=True,
                    ticks_on=True, colours=default_colours, alpha=0.85, userdefined_limits = False):

    """
    The tiling2_s argument should be a list of tiling2 objects.
    """

    figure = plt.figure(frameon = True)
    figure.set_size_inches(figure_size,figure_size)
    axis = figure.add_subplot(111)
    for tiling2 in tiling2_s:
        for (i,face) in enumerate(tiling2.faces):
            l = describe_polygon_path([(v.x, v.y) for v in cycle(face)])
            patch = patches.PathPatch(l, facecolor=colours[(len(face)-3)%len(colours)], lw=1.3, ec='k', alpha=alpha)
            axis.add_patch(patch)
    plt.axis('scaled')
    if userdefined_limits != False:
        axis.set_xlim(-userdefined_limits[0][0],userdefined_limits[0][1])
        axis.set_ylim(-userdefined_limits[1][0],userdefined_limits[1][1])
    axis.axis()
    if grid_on == True :
        axis.grid(True)
    if ticks_on == False:
        axis.set_xticks([])
        axis.set_yticks([])
    return figure

