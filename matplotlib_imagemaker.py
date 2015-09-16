import os
import matplotlib.pyplot as plt

from polygon_count import *
from tiling3_matplotlib import tiling3_s_3d_subplot
from tiling2_matplotlib import tiling2_s_flattened_subplot
from data_line_matplotlib import line_plot_2d
from simultaneous_plot import simultaneous_plot
from restrict32 import restrict32
from progress import progressenumerate


class Imagemaker(object):

    def image(self, tiling):
        """
        This function should create an image.
        """
        raise NotImplementedError("You need to define this in a subclass")

    def store_image(self, tiling, name):
        fig = self.image(tiling)
        fig.save(name)
        fig.close()

    def animation(self, list_of_tilings, folder):
        """
        Given a list of images, this stores them with convenient numbered
        filenames in the given folder.
        """
        folder = folder+"_png"
        for (i, tiling) in progressenumerate(list_of_tilings):
            filename = "img%06d.png"%(i+1,)
            store_image(self, tiling, os.path.join(folder, filename))


class SimpleImageMaker(Animator):

    def __init__(self,
                 tiling3_s_number_of_rows=1,
                 tiling3_s_number_of_columns=1,
                 tiling3_s_position_code=1,
                 colours=default_intersection_colours,
                 plane_z0_on=False,
                 restrict32_intersection_on=False,
                 tiling3_edges_on=True,
                 tiling3_faces_on=True,
                 tiling3_edge_colours=['black'],
                 axis_limit=False,
                 elevation=30,
                 azimuth=30,
                 save_name='tiling3_image',
                 folder='demos/tiling3animation',
                 save_on=True,
                 plane_z0_alpha=0.2,
                 restrict32_alpha=0.8,
                 tiling3_faces_alpha=0.8,
                 tiling3_edges_alpha=0.8):
        self.tiling3_s_number_of_rows = tiling3_s_number_of_rows
        self.tiling3_s_number_of_columns = tiling3_s_number_of_columns
        self.tiling3_s_position_code = tiling3_s_position_code
        self.colours = colours
        self.plane_z0_on = plane_z0_on
        self.restrict32_intersection_on = restrict32_intersection_on
        self.tiling3_edges_on = tiling3_edges_on
        self.tiling3_faces_on = tiling3_faces_on
        self.tiling3_edge_colours = tiling3_edge_colours
        self.axis_limit = axis_limit
        self.elevation = elevation
        self.azimuth = azimuth
        self.save_name = save_name
        self.folder = folder
        self.save_on = save_on
        self.plane_z0_alpha = plane_z0_alpha
        self.restrict32_alpha = restrict32_alpha
        self.tiling3_faces_alpha = tiling3_faces_alpha
        self.tiling3_edges_alpha = tiling3_edges_alpha

    def make_snapshot(self):
        ### this should be the current content of tiling3_s_3d_subplot
