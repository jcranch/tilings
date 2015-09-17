from data_line_matplotlib import line_plot_2d
from simultaneous_plot import simultaneous_plot
from restrict32 import restrict32
from progress import progressenumerate
from vector3 import Vector3
from restrict32 import restrict32
from common import cycle

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import pyplot as plt
import numpy as np
import os

class ImageMaker(object):

    def image(self, tiling):
        """
        This function should create an image.
        """
        raise NotImplementedError("You need to define this in a subclass")

    def store_image(self, tiling_s,  save_name = 'tiling_image', folder = 'demos/tiling_static'):
        if not os.path.exists(folder):
            os.makedirs(folder)
        figure = plt.figure(figsize = self.figure_size)
        self.image(tiling_s)
        figure.savefig(os.path.join(folder, save_name))
        plt.close()

    def animation(self, list_of_tiling_s, folder):
        """
        Given a list of images, this stores them with convenient numbered
        filenames in the given folder.
        """
        folder = folder+"_png"
        for (i, tiling_s) in progressenumerate(list_of_tiling_s):
            file_name = "img%06d.png"%(i+1,)
            self.store_image(tiling_s, file_name, folder)
            
            
class Tiling3ImageMaker(ImageMaker):

    def __init__(self,
                 colours=default_intersection_colours,
                 figure_size = [5,5],
                 plane_z0_on=False,
                 restrict32_intersection_on=False,
                 tiling3_edges_on=True,
                 tiling3_faces_on=True,
                 number_of_rows = 1,
                 number_of_columns = 1,
                 position_code = 1,
                 edge_colours=['black'],
                 tiling3_axis_limit=False,
                 elevation=30,
                 azimuth=30,
                 plane_z0_alpha=0.2,
                 tiling2_alpha=0.8,
                 tiling3_faces_alpha=0.8,
                 edges_alpha=0.8):
        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns
        self.position_code = position_code
        self.figure_size = figure_size
        self.colours = colours
        self.plane_z0_on = plane_z0_on
        self.restrict32_intersection_on = restrict32_intersection_on
        self.tiling3_edges_on = tiling3_edges_on
        self.tiling3_faces_on = tiling3_faces_on
        self.edge_colours = edge_colours
        self.tiling3_axis_limit = tiling3_axis_limit
        self.elevation = elevation
        self.azimuth = azimuth
        self.plane_z0_alpha = plane_z0_alpha
        self.tiling2_alpha = tiling2_alpha
        self.tiling3_faces_alpha = tiling3_faces_alpha
        self.edges_alpha = edges_alpha

    def tiling3_image(self,tiling3_s):

        '''
        This function is used to create 3D subplots for tiling3 objects.
            This function creates a 3D subplot that is able to produce images of :
        - a Tiling3 instance's edges and/or faces,
        - a Tiling2 instance's edges and faces on the plane z = 0,
        - the plane z = 0.
        Number of rows and number of columns determines how the figure is subdivided into equal areas
        and the position code decides which area the subplot is plotted in.
        To plot in the area in the i^{th} row and j^{th} the position code should be
        j + (i-1)*j .
        For example to plot in the top right quarter of a picture we use
        number_of_rows = 2, number_of_columns = 2, position_code = 1.
        '''
        axis = plt.subplot(self.number_of_rows, self.number_of_columns, self.position_code, 
                           projection='3d', aspect='equal')
        
        tiling3_axis_limit = self.tiling3_axis_limit
        if tiling3_axis_limit == False:
            bound = 0
            for tiling_3 in tiling3_s:
                if tiling_3.vertices:
                    contender = max([abs(tiling_3.maxx()), abs(tiling_3.minx()),
                    abs(tiling_3.miny()), abs(tiling_3.maxy()),
                    abs(tiling_3.minz()), abs(tiling_3.maxz())])
                    if contender > bound:
                        bound = contender
            tiling3_axis_limit = [[-bound-1,bound+1]]*3
        polygon_tiles = []
        axis.grid(False)
        axis.set_xticks([])
        axis.set_yticks([])
        axis.set_zticks([])
        axis.set_axis_off()
        axis.set_xlim(tiling3_axis_limit[0])
        axis.set_ylim(tiling3_axis_limit[1])
        axis.set_zlim(tiling3_axis_limit[2])
        axis.view_init(self.elevation, self.azimuth)
        lines = []
        x_s = []
        y_s = []
        z_s = []
        for (k, tiling3) in enumerate(tiling3_s):
            if self.tiling3_edges_on == True:
                for (j, face) in enumerate(tiling3.faces):
                    for edge in list(face):
                        lines.append(axis.plot([], [], [], '', color=self.edge_colours[k%len(self.edge_colours)],
                                               alpha=self.edges_alpha)[0])
                        vertex_1 = [list(edge)[0][1],list(edge)[0][2],list(edge)[0][3]]
                        vertex_2 = [list(edge)[1][1],list(edge)[1][2],list(edge)[1][3]]
                        x_s += [[vertex_1[0],vertex_2[0]]]
                        y_s += [[vertex_1[1],vertex_2[1]]]
                        z_s += [[vertex_1[2],vertex_2[2]]]
                for (j, line) in enumerate(lines):
                    line.set_data(x_s[j],y_s[j])
                    line.set_3d_properties(z_s[j])

            if self.tiling3_faces_on == True:
                if self.tiling3_edges_on == True:
                    for (j, face) in enumerate(tiling3.faces):
                        polygon_tiles.append(axis.add_collection3d(Poly3DCollection([[(v.x,v.y,v.z) for v in cycle(face)]],
                        facecolor = self.colours[(len(face)-3)%len(self.colours)],
                        edgecolor =self.edge_colours[k%len(self.edge_colours)],
                        alpha = self.tiling3_faces_alpha)))

            if self.restrict32_intersection_on == True:
                for (j, face) in enumerate(restrict32(tiling3).faces):
                    polygon_tiles.append(axis.add_collection3d(Poly3DCollection([[(v.x,v.y,0) for v in cycle(face)]],
                    facecolor=self.colours[(len(face)-3)%len(self.colours)],
                    edgecolor=self.tiling3_edge_colours[k%len(self.tiling3_edge_colours)], alpha = self.tiling2_alpha)))

        if self.plane_z0_on == True:
            axis.add_collection3d(Poly3DCollection([[(axis_limit[0][0],axis_limit[1][0],0),(axis_limit[0][0],axis_limit[1][1],0),
                                                     (axis_limit[0][1],axis_limit[0][1],0),(axis_limit[0][1],axis_limit[1][0],0)]],
                                                   facecolor ='white',
                                                   edgecolor ='black', alpha = self.plane_z0_alpha))
        return axis
    def image(self,tiling3_s):
        return self.tiling3_image(tiling3_s)
        
class Tiling2ImageMaker(ImageMaker):
    def __init__(self,
                 colours=default_intersection_colours,
                 figure_size = [5,5],
                 number_of_rows = 1,
                 number_of_columns = 1,
                 position_code = 1,
                 edge_colours=['black'],
                 tiling2_axis_limit = False,
                 tiling2_alpha=0.8,
                 edges_alpha=0.8):

        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns
        self.position_code = position_code
        self.figure_size = figure_size
        self.colours = colours        
        self.edge_colours = edge_colours
        self.tiling2_axis_limit = tiling2_axis_limit
        self.tiling2_alpha = tiling2_alpha
        self.edges_alpha = edges_alpha

    
    def tiling2_image(self,tiling2_s):
        '''
        This function is used to create 2D subplots for tiling2 objects.

        Number of rows and number of columns determines how the figure is subdivided into equal areas
        and the position code decides which area the subplot is plotted in. 

        To plot in the area in the i^{th} row and j^{th} the position code should be 
        j + (i-1)*j . 

        For example to plot in the top right quarter of a picture we use 
        number_of_rows = 2, number_of_columns = 2, position_code = 1.
        '''
        tiling2_limits = self.tiling2_axis_limit
        if tiling2_limits == False:
            bound = 0
            for tiling_2 in tiling2_s:
                if tiling_2.vertices:
                    contender = max([abs(tiling_2.maxx()), abs(tiling_2.minx()),
                    abs(tiling_2.miny()), abs(tiling_2.maxy())])
                    if contender > bound:
                        bound = contender
            tiling2_limits = [[-bound-1,bound+1]]*2

        axis = plt.subplot(self.number_of_rows, self.number_of_columns,self.position_code, 
                           xlim = tiling2_limits[0], ylim = tiling2_limits[1], aspect='equal', frameon = False)
        axis.get_xaxis().set_visible(False)
        axis.get_yaxis().set_visible(False)
        patches = []
        grand_n = 0
        for (k,tiling2) in enumerate(tiling2_s):
            for (n,face) in enumerate(tiling2.faces):
                patches.append(axis.add_patch(plt.Polygon(0 * np.array([(v.x, v.y) for v in cycle(face)]),
                facecolor = self.colours[(len(face)-3)%len(self.colours)], edgecolor = self.edge_colours[k%len(self.edge_colours)] , ec='k', 
                                                          alpha = self.tiling2_alpha)))
                patches[grand_n+n].set_xy(np.array([(v.x, v.y) for v in cycle(face)]))
            grand_n += 1      
        return axis
    def image(self, tiling2_s):
        return self.tiling2_image(tiling2_s)
