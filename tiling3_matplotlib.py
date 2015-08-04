from periodic_tiling3 import cubic_tiling3
from matrix3 import rotate_x, rotate_y,rotate_z
from vector3 import Vector3
from restrict32 import restrict32
from common import cycle

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import pyplot as plt
import numpy as np



default_intersection_colours = ['orange','lime','red','aqua','magenta','darkgreen','lightblue','gold','black','purple','blue','darkred','darkblue','lightgreen']




def matplotlib_display_tiling3(tiling3,tiling_3_on = True,axis_3D_intersection_tiling2_on = True,\
                               intersection_colours = default_intersection_colours, intersection_alpha = 0.5,\
                               plane_z0_on = False ,plane_z0_alpha = 0.3,tiling3_colours = ['black'],plane_z0_colour = 'blue',\
                               tiling3_alpha = 0.5,initial_elevation = 20, initial_azimuth = 30, axis_3D_on = False,\
                               axis_3D_grid_on = False, user_defined_axis_3D_limit = False,\
                               save_on = True, save_name = 'demos/tiling3_figure'):
    figure = plt.figure()
    axis = Axes3D(figure)
    tiling2 = restrict32(tiling3)
    plt.axis('scaled')
    if axis_3D_grid_on == True:
        axis.grid(True)
    if axis_3D_on == False:
        axis.get_xaxis().set_visible(False)
        axis.get_yaxis().set_visible(False)
        axis.axis('off')
    if user_defined_axis_3D_limit == False:
        absolute_largest = max(abs(tiling3.minx()),tiling3.maxx(),\
                               abs(tiling3.miny()),tiling3.maxy(),
                               abs(tiling3.minz()),tiling3.maxz())
        axis.set_xlim(-absolute_largest-1,absolute_largest+1)
        axis.set_ylim(-absolute_largest-1,absolute_largest+1)
        axis.set_zlim(-absolute_largest-1,absolute_largest+1)
    else :
        axis.set_xlim(user_defined_axis_3D_limit[0][0][0],user_defined_axis_3D_limit[0][0][1])
        axis.set_ylim(user_defined_axis_3D_limit[0][1][0],user_defined_axis_3D_limit[0][1][1])
        axis.set_zlim(user_defined_axis_3D_limit[0][2][0],user_defined_axis_3D_limit[0][2][1])
    polygon_tiles = []
    if axis_3D_intersection_tiling2_on == True:
        for (j,face) in enumerate(tiling2.faces.keys()):
            polygon_tiles += [axis.add_collection3d(Poly3DCollection([[(v.x,v.y,0) for v in cycle(face)]],\
            facecolor = intersection_colours[len(face)-3],edgecolor = 'black',alpha = intersection_alpha))]
    if plane_z0_on == True:
        axis.add_collection3d(Poly3DCollection([[(absolute_largest,absolute_largest,0),(absolute_largest,-absolute_largest,0),\
                                                 (-absolute_largest,-absolute_largest,0),(-absolute_largest,absolute_largest,0)]],\
                                               facecolor = plane_z0_colour,\
                                               edgecolor = 'black',alpha = plane_z0_alpha))
    lines = []
    for (j,edge) in enumerate(tiling3.edges.keys()):
        point_1 = [list(edge)[0][1],list(edge)[0][2],list(edge)[0][3]]
        point_2 = [list(edge)[1][1],list(edge)[1][2],list(edge)[1][3]]
        co_ordinates = zip(point_1,point_2)
        axis.plot(co_ordinates[0],co_ordinates[1],co_ordinates[2],'',color = tiling3_colours[j%len(tiling3_colours)],alpha = 0.5)
    if save_on == True:
        plt.savefig(save_name)

    return figure
