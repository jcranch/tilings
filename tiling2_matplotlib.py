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
    

'''
Some code for animating plotygons in preparation for animating 2d tiling.
'''

'''

Function should take a list of polygons as described before,
as well as a list of functions of the same length of the list of polygons
where each function is a function of the form 

def f(np.array(polygon), i):
    ......
    return np.array(...)

'''
def animate_plotygons(polygons, list_of_animation_functions,
                      colours=default_colours, alpha=0.85):

    figure = plt.figure(figsize=(8,8))
    axis = figure.add_axes([0,0,1,1], xlim = (-11, 11), ylim = (-11, 11),\
    xticks = range(10), yticks= range(10) , aspect='equal', frameon = True)
    axis.grid(True)
    patches = []
    for polygon in polygons:
        patches += [axis.add_patch(plt.Polygon(0 * np.array(polygon), facecolor = colours[polygons.index(polygon)%len(colours)], ec='k', alpha=alpha))]
    # What is always being plotted during animation (in this case nothing, just a blank point).
    def initial():  
        for index in range(len(patches)):
            patches[index].set_xy([[0,0],[0,0]])
        return patches
    # What is being displayed on the i^{th} frame. 
    # The k^{th} polygon is transformed by k^{th} function in list_of_animation_functions for all i.
    def animates(i): 
        for index in range(len(patches)): 
            patches[index].set_xy(list_of_animation_functions[index](np.array(polygons[index]),i))
        return patches 
    animating = animation.FuncAnimation(figure, animates, init_func = initial, frames = 10, interval=10,blit = True)
    plt.show()
    return None 

