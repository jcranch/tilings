from matrix4 import rotate_wx, rotate_wy, rotate_wz, rotate_xy, rotate_xz, rotate_yz
from vector4 import Vector4
from restrict43 import restrict43
from restrict32 import restrict32
from common import cycle
from tiling3_matplotlib import default_intersection_colours

import os
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def uniform_rotate_transformation(tiling3, i, rate = 20.0, theta_wx = np.pi, theta_wy= np.pi,theta_wz= np.pi, theta_xy= np.pi, theta_xz= np.pi, theta_yz= np.pi):
    rotation_matrix = rotate_wx(theta_wx+i/rate) * rotate_wy(theta_wy+i/rate)*rotate_wz(theta_wz+i/rate)\
    *rotate_xy(theta_xy+i/rate)*rotate_xz(theta_xz+i/rate)*rotate_yz(theta_yz*i/rate)
    return tiling3.deform(rotation_matrix)

def rotate_wz_transformation(tiling4,i,rate):
    rotation_matrix = rotate_wz(i/rate)
    return tiling3.deform(rotation_matrix)

def translate_z(tiling3, i, rate = 20.0):
    max_z = tiling4.maxz()
    return tiling4.translate(Vector4(0,0,0,max_z-i/rate))
def identity_transformation(tiling, i = 0):
    return tiling

def scale(i,scalar = -1/1.0):
    return float(i * scalar)

def elevation_transformation_1(i):
    return np.sin(i/10.0)*0.0

def azimuth_transformation_1(i):
    return i/10.0

def full_animation_43(tiling4,frames = 10,transformation_function = uniform_rotate_transformation,
    polygon_count_on = True, tiling_3_on = True, intersection_tiling2_on = True,
    intersection_colours = default_intersection_colours, intersection_alpha = 0.5,
    plane_z0_on = True ,rotate_view_on = True,plane_z0_alpha = 0.3,
    elevation_transformation = elevation_transformation_1, azimuth_transformation = azimuth_transformation_1,
    tiling3_colours = ['black'],plane_z0_colour = 'white',tiling3_alpha = 0.5,
    initial_elevation = 20, initial_azimuth = 30, axis_limit = 2.5, axis_3D_on = False, axis_3D_grid_on = False,
    axis_3D_intersection_tiling2_on = True, save_on = True, save_name = 'restrict43_animation', print_progress_on = True):
    '''
    This function creates a series of png files saved to a demos folder that show the desired polytope intersecting 
    z = 0.
    '''
    folder_name = "demos/"+save_name+"_png/"
    
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    raw_n_gon_count_results = []
    tiling2_faces = []
    tiling3_edges = []
    for frame in range(frames):
        transforming_4d_tiling = transformation_function(tiling4, frame)
        transforming_3d_tiling = restrict43(transforming_4d_tiling)
        transforming_2d_intersection = restrict32(transforming_3d_tiling).clip(-20,20,-20,20)
        if polygon_count_on == True:
            raw_n_gon_count_results += [transforming_2d_intersection.face_count_information()]
        if tiling_3_on == True:
            tiling3_edges += [transforming_3d_tiling.faces.keys()]
        if intersection_tiling2_on == True:
            tiling2_faces += [transforming_2d_intersection.faces.keys()]

    # For polygon count.
    distinct_n_gons_found = []
    for dictionary_of_n_gons in raw_n_gon_count_results:
        for n_gon in dictionary_of_n_gons:
            if n_gon not in distinct_n_gons_found:
                distinct_n_gons_found += [n_gon]
    data_lines = dict([(n_gon,[]) for n_gon in distinct_n_gons_found])

    max_number_of_faces = 0.0
    for frame in range(frames):
        for n_gon in distinct_n_gons_found:
            if n_gon in raw_n_gon_count_results[frame]:
                data_lines[n_gon] += [raw_n_gon_count_results[frame][n_gon]]
                if raw_n_gon_count_results[frame][n_gon] > max_number_of_faces:
                    max_number_of_faces = raw_n_gon_count_results[frame][n_gon]
            else :
                data_lines[n_gon] += [0.0]

    figure = plt.figure(figsize=(20,15))

    #3D Plot
    if tiling_3_on == True:
        axis_3D = plt.subplot(222, projection = '3d')
        axis_3D.set_xlim((-axis_limit, axis_limit))
        axis_3D.set_ylim((-axis_limit, axis_limit))
        axis_3D.set_zlim((-axis_limit, axis_limit))
        if axis_3D_grid_on == False:
            axis_3D.grid(False)
        if axis_3D_on == False:
            axis_3D.get_xaxis().set_visible(False)
            axis_3D.get_yaxis().set_visible(False)
            axis_3D.axis('off')
        axis_3D.view_init(initial_elevation, initial_azimuth)
        lines3D = []
    #2D Plot
    if intersection_tiling2_on == True:
        axis_2D = plt.subplot(221, xlim = (-5, 5.02), ylim = (-5, 5.02), aspect='equal', frameon = False)
        axis_2D.get_xaxis().set_visible(False)
        axis_2D.get_yaxis().set_visible(False)
    #Polygon Count Plot
    lines_face_count = []
    if polygon_count_on == True:
        axis_polygon_count = plt.subplot(815, \
        xlim = (-1.01, frames+frames/10), ylim = (-0.01, max_number_of_faces + 1 ),frameon = False)
        axis_polygon_count.set_xlabel("Frame", fontsize = 18)
        axis_polygon_count.set_ylabel("Polygon Count", fontsize = 18)
        axis_polygon_count.grid(True)
        lines_tiling3 = []
        for n_gon in data_lines:
            lines_face_count += [axis_polygon_count.plot([],[],'', label = str(n_gon),color = intersection_colours[n_gon-3],\
                                                         alpha = intersection_alpha)[0]]

    for i in range(frames):
        #face_count
        if polygon_count_on == True:
            x_s = range(1,i+2)
            for (line,n_gon) in zip(lines_face_count,data_lines):
                y_s = data_lines[n_gon][:i+1]
                line.set_data(x_s,y_s)
            axis_polygon_count.legend(loc = 'upper right',framealpha = 1.0, fancybox = True)
        #3D
        lines = []
        if tiling_3_on == True:
            axis_3D.clear()
            if axis_3D_grid_on == False:
                axis_3D.grid(False)
            if axis_3D_on == False:
                axis_3D.get_xaxis().set_visible(False)
                axis_3D.get_yaxis().set_visible(False)
                axis_3D.axis('off')
            axis_3D.set_xlim((-axis_limit, axis_limit))
            axis_3D.set_ylim((-axis_limit, axis_limit))
            axis_3D.set_zlim((-axis_limit, axis_limit))
            axis_3D.view_init(initial_elevation, initial_azimuth)
            if plane_z0_on == True:
                axis_3D.add_collection3d(Poly3DCollection([[(axis_limit,axis_limit,0),(axis_limit,-axis_limit,0),\
                                                         (-axis_limit,-axis_limit,0),(-axis_limit,axis_limit,0)]],\
                                                       facecolor = plane_z0_colour,\
                                                       edgecolor = 'black',alpha = plane_z0_alpha))
            if rotate_view_on == True:
                axis_3D.view_init(initial_elevation + elevation_transformation(i),\
                initial_azimuth + azimuth_transformation(i))
                figure.canvas.draw()
            polygon_tiles = []
            if axis_3D_intersection_tiling2_on == True:
                for (j,face) in enumerate(tiling2_faces[i]):
                    polygon_tiles += [axis_3D.add_collection3d(Poly3DCollection([[(v.x,v.y,0) for v in cycle(face)]],\
                    facecolor = intersection_colours[len(face)-3],edgecolor = 'black',alpha = intersection_alpha))]
            x_s = []
            y_s = []
            z_s = []
            for (j,face) in enumerate(tiling3_edges[i]):
                for edge in list(face):
                    lines  += [axis_3D.plot([],[],[],'',color = tiling3_colours[j%len(tiling3_colours)],alpha = tiling3_alpha)[0]]
                    vertex_1 = [list(edge)[0][1],list(edge)[0][2],list(edge)[0][3]]
                    vertex_2 = [list(edge)[1][1],list(edge)[1][2],list(edge)[1][3]]
                    x_s += [[vertex_1[0],vertex_2[0]]]
                    y_s += [[vertex_1[1],vertex_2[1]]]
                    z_s += [[vertex_1[2],vertex_2[2]]]
            for (j,line) in enumerate(lines):
                line.set_data(x_s[j],y_s[j])
                line.set_3d_properties(z_s[j])
       #2D
        patches = []
        if intersection_tiling2_on == True:
            axis_2D.clear()
            for (n,face) in enumerate(tiling2_faces[i]):
                patches += [axis_2D.add_patch(plt.Polygon(0 * np.array([(v.x, v.y) for v in cycle(face)])\
                , facecolor = intersection_colours[(len(face)-3)%len(intersection_colours)], ec='k', alpha = intersection_alpha))]
                patches[n].set_xy(np.array([(v.x, v.y) for v in cycle(face)]))
        if save_on == True:
            figure.savefig("demos/"+save_name+"_png/"+str(i))
        if print_progress_on == True:
            print str(int(float(i)/frames*100)) + '% completed.'
            
    return None
