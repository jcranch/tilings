
from periodic_tiling3 import cubic_tiling3
from matrix3 import rotate_x, rotate_y,rotate_z
from vector3 import Vector3
from restrict32 import restrict32
from common import cycle

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation
import numpy as np
import itertools



def rotate_transformation(tiling3, i, theta_x = 0.0, theta_y = 0.0,theta_z = 30.0):
    rotation_matrix = rotate_x(theta_x*i/1000.0) * rotate_y(theta_y*i/1000.0)*rotate_z(theta_z*i/1000.0)
    return tiling3.deform(rotation_matrix)

def identity_transformation(tiling, i = 0):
    return tiling

def scale(i,scalar = -1/1.0):
    return float(i * scalar)

def elevation_transformation_1(i):
    return np.sin(i/10.0)*0.0 

def azimuth_transformation_1(i):
    return i/10.0

def special_transformation_1(tiling3, i, theta_x = 5**0.5*10.0, theta_y = 2**0.5*10.0,theta_z = 3**0.5*10.0):
    rotation_matrix = rotate_x(theta_x*i/1000.0) * rotate_y(theta_y*i/1000.0)*rotate_z(theta_z*i/1000.0)
    return tiling3.deform(rotation_matrix).translate(Vector3(np.sin(3**0.5*i/100.0),np.sin(2**0.5*i/100.0), np.sin(2**0.5*i/10.0)))

default_intersection_colours = ['orange','lime','red','aqua','magenta','darkgreen','lightblue','gold','black','purple','blue','darkred','darkblue','lightgreen']





def full_animation_32(frames = 100,ploygon_count_on = True, tiling_3_on = True, intersection_tiling2_on = True, \
    tiling3 = cubic_tiling3(((-1,1),(-1,1),(-1,1))).translate(Vector3(0,0,-0.000051)),\
    transformation_function = special_transformation_1,\
    intersection_colours = default_intersection_colours, intersection_alpha = 0.5,\
    plane_z0_on = True ,rotate_view_on = True,\
    plane_z0_alpha = 0.3,\
    elevation_transformation = elevation_transformation_1, azimuth_transformation = azimuth_transformation_1,\
    tiling3_colours = ['black'],plane_z0_colour = 'white',\
    tiling3_alpha = 0.5,\
    initial_elevation = 20, initial_azimuth = 30, axis_limit = 2.5, axis_3D_on = False, axis_3D_grid_on = False,
    axis_3D_intersection_tiling2_on = True, save_on = True, save_name = 'restrict32_animation', print_progress_on = True):
    '''
    Arguments:
    - frames : the number of times we wish to aply the transformation function and record the results.
    - blit_on : this argument should be either True or False and determine whether or not blit is on or off in the animation,
    - polygon_count_on : this argument should be either True or False and determine whether or not polygon count is on or off in the animation,
    - tiling_3_on : this argument should be either True or False and determine whether or not tiling3 is on or off in the animation,
    - intersection_tiling2_on : this argument should be either True or False and determine whether or not the intersection tiling2 is on or off in the animation,
    - transformation_function : the transformation we wish to apply th the tiling3. This function shouls return a tiling3.
    - intersection_colours : the colours used in the intersection tiling 2.
    - intersection_alpha : determines the transparancy of these colours should be a number n s.t. 0 <= n <= 1.
    - plane_z0_on : this argument should be either True or False and determine whether or not the plane z = 0 is on or off in the animation,
    - rotate_view_on : this argument should be either True or False and determine whethter or not the tiling3 animation will have a fixed view or not.
    - elevation_transformation : if rotate_view_on == True then this function determines how the elevation changes with respect to each frame and ret
    - azimuth_transformation : similar to elevation_transformation.
    - tiling3_colours : determines the colour of the edges in the tiling3.
    - tiling3_alpha : determines the transparancy of these colours should be a number n s.t. 0 <= n <= 1.
    - save_on : this argument should be either True or False and determine whether or not the animation is saved as a .png file.
    - save_name : the name you wish to save the image as in save_on == True.
    - print_progress_on : this argument should be either True or False and determines if you want the progress of animation to be printed.
    '''
    raw_n_gon_count_results = []
    tiling2_faces = []
    tiling3_edges = []
    for frame in range(frames):
        transforming_3d_tiling = transformation_function(tiling3,frame)
        transforming_2d_intersection = restrict32(transforming_3d_tiling).clip(-20,20,-20,20)
        if ploygon_count_on == True:
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
    if ploygon_count_on == True:
        axis_polygon_count = plt.subplot(815, \
        xlim = (-1.01, frames+frames/10), ylim = (-0.01, max_number_of_faces + 1 ),frameon = False)
        axis_polygon_count.set_xlabel("Frame", fontsize = 18)
        axis_polygon_count.set_ylabel("Polygon Count", fontsize = 18)
        axis_polygon_count.grid(True)
        lines_tiling3 = []
        for n_gon in data_lines:
            lines_face_count += [axis_polygon_count.plot([],[],'', label = str(n_gon),color = intersection_colours[n_gon-3],\
                                                         alpha = intersection_alpha)[0]]
        
    
    
    def animate(i):
        #face_count
        if ploygon_count_on == True: 
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
                , facecolor = intersection_colours[len(face)-3], ec='k', alpha = intersection_alpha))]    
                patches[n].set_xy(np.array([(v.x, v.y) for v in cycle(face)]))   
        if save_on == True:
            figure.savefig(save_name + '_' + str(i) + '.png')
        if print_progress_on == True:
            print str(int(float(i)/frames*100)) + '% completed.'
        return lines_face_count, lines, patches
    return animation.FuncAnimation(figure, animate, frames = frames, interval = 20, blit = True)
        
    
    
    
    
    
   
