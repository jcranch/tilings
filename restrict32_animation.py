from periodic_tiling3 import cubic_tiling3
from matrix3 import rotate_x, rotate_y,rotate_z
from vector3 import Vector3
from restrict32 import restrict32
from common import cycle


import numpy as np
from matplotlib import animation
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches


# This an auxillary transformation function to be called later on the animation.
# It slowly rotates the tiling3 with respect to x,y,z.

def rotate_transformation(tiling3, i, theta_x = 30.0, theta_y = 30.0,theta_z = 30.0):
    rotation_matrix = rotate_x(theta_x*i/1000.0) * rotate_y(theta_y*i/1000.0)*rotate_z(theta_z*i/1000.0)
    return tiling3.deform(rotation_matrix)


#For now I have settled for the single colour 'lime' until new colour system is added successfully.

def animate_restrict32(tiling3 = cubic_tiling3(((-3,3),(-3,3),(-3,3))).translate(Vector3(0,0,-0.51)),\
    transformation_function = rotate_transformation, colour = 'lime', grid_on = True, alpha = 0.75):
    '''
    This function takes a tiling3 and transforms it using the transformation function and displays an animation 
    '''
    figure = plt.figure(figsize=(8,8))
    if grid_on == True:
        axis = figure.add_axes([0,0,1,1], xlim = (-10, 10.02), ylim = (-10, 10.02),\
        xticks = range(-10,11), yticks= range(-10,11) , aspect='equal', frameon = True, alpha = alpha)
        axis.grid(True)
    else :
        axis = figure.add_axes([0,0,1,1], xlim = (-5, 5.02), ylim = (-5, 5.02),\
        xticks = [], yticks= [] , aspect='equal', frameon = True, alpha = alpha)
    intersection_2d = restrict32(tiling3).clip(-20,20,-20,20)
    def initial(): 
        '''
    This is the starting frame and is permanant so it will be present on all frames. 
    So we want this to be blank in this case.
    '''
        return []
    def animate(i):
        '''
    This is what is animated during the i^{th} frame of the video. 
    In this case we transform our tiling3 using our transformation function
    and display the intersection with z = 0 .
    '''
        transforming_3d_tiling = transformation_function(tiling3,i)
        transforming_2d_intersection = restrict32(transforming_3d_tiling).clip(-20,20,-20,20)
        patches = []
        for (n,face) in enumerate(transforming_2d_intersection.faces.keys()):
            patches += [axis.add_patch(plt.Polygon(0 * np.array([(v.x, v.y) for v in cycle(face)])\
            , facecolor = colour, ec='k', alpha = alpha))]    
            patches[n].set_xy(np.array([(v.x, v.y) for v in cycle(face)]))
        return patches
    animating = animation.FuncAnimation(figure, animate, init_func = initial, frames = 1000, interval=10,blit = True)
    plt.show()
    return None 




def animate_restrict32_union_shadow(tiling3 = cubic_tiling3(((-3,3),(-3,3),(-3,3))).translate(Vector3(0,0,-0.51)),\
    transformation_function = rotate_transformation, grid_on = True):
    '''
    This function takes a whole of a tiling3 and transforms it using the transformation function and displays an animation.
    This function returns the shadow of the whole tiling passing though z = 0.
    '''
    figure = plt.figure(figsize=(8,8))
    if grid_on == True:
        axis = figure.add_axes([0,0,1,1], xlim = (-10, 10.02), ylim = (-10, 10.02),\
        xticks = range(-10,11), yticks= range(-10,11) , aspect='equal', frameon = True, alpha = 1.0)
        axis.grid(True)
    else :
        axis = figure.add_axes([0,0,1,1], xlim = (-5, 5.02), ylim = (-5, 5.02),\
        xticks = [], yticks= [] , aspect='equal', frameon = True, alpha = 1.0)
    intersection_2d = restrict32(tiling3).clip(-20,20,-20,20)
    def initial(): 
        '''
    This is the starting frame and is permanant so it will be present on all frames. 
    So we want this to be blank in this case.
    '''
        return []
    def animate(i):
        '''
    This is what is animated during the i^{th} frame of the video. 
    In this case we transform our tiling3 using our transformation function
    and display the intersection with z = 0 .
    '''
        transforming_3d_tiling = transformation_function(tiling3,i)
        transforming_2d_intersection = restrict32(transforming_3d_tiling).clip(-20,20,-20,20)
        patches = []
        for (n,face) in enumerate(transforming_2d_intersection.faces.keys()):
            patches += [axis.add_patch(plt.Polygon(0 * np.array([(v.x, v.y) for v in cycle(face)])\
            , facecolor = 'black', ec='k', alpha = 1.0))]    
            patches[n].set_xy(np.array([(v.x, v.y) for v in cycle(face)]))
        return patches
    animating = animation.FuncAnimation(figure, animate, init_func = initial, frames = 1000, interval=10,blit = True)
    plt.show()
    return None 
    
    # The following function is designed to save each frame of our restrict32 animation for developing mp4 files.
    
    
    def animate_restrict32_manual_save(frames = 10, tiling3 = cubic_tiling3(((-3,3),(-3,3),(-3,3))).translate(Vector3(0,0,-0.51)),\
    transformation_function = rotate_transformation, colour = 'lime', grid_on = True, alpha = 0.75,\
    show_on = True, save_on = True, save_name = 'animate_restrict32'):
    '''
    This function takes a tiling3 and transforms it using the transformation function and displays an animation. 
    '''
    for frame in range(frames):
        figure = plt.figure(figsize = (8,8))
        if grid_on == True:
            axis = figure.add_axes([0,0,1,1], xlim = (-10, 10.02), ylim = (-10, 10.02),\
            xticks = range(-10,11), yticks= range(-10,11) , aspect='equal', frameon = True, alpha = alpha)
            axis.grid(True)
        else :
            axis = figure.add_axes([0,0,1,1], xlim = (-5, 5.02), ylim = (-5, 5.02),\
            xticks = [], yticks= [] , aspect='equal', frameon = True, alpha = alpha)
        transforming_3d_tiling = transformation_function(tiling3,frame)
        transforming_2d_intersection = restrict32(transforming_3d_tiling).clip(-20,20,-20,20)
        patches = []
        for (n,face) in enumerate(transforming_2d_intersection.faces.keys()):
            patches += [axis.add_patch(plt.Polygon(0 * np.array([(v.x, v.y) for v in cycle(face)])\
            , facecolor = colour, ec='k', alpha = alpha, lw = 2))]    
            patches[n].set_xy(np.array([(v.x, v.y) for v in cycle(face)]))
        if show_on == True:
            plt.show()
        if save_on == True:
            plt.savefig(save_name + str(frame)+".png")
    return None 




