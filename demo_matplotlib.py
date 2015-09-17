from math import pi

from vector2 import Vector2
from vector3 import Vector3
from matrix3 import rotate_x, rotate_y, rotate_z
from tiling3_matplotlib import tiling3_s_3d_subplot
from tiling3_polyhedron import tetrahedron, octahedron, cube, icosahedron, dodecahedron
from matplotlib_imagemaker import Tiling3ImageMaker, Tiling2ImageMaker
from tiling2_polygon import regular_polygon

tiling2_image_creator = Tiling2ImageMaker()
tiling3_image_creator = Tiling3ImageMaker()
if __name__=="__main__":
    platonic_solids = [tetrahedron(), cube(), octahedron(), dodecahedron(), icosahedron()]
    for platonic_solid in platonic_solids:
        tiling3_image_creator.store_image([platonic_solid.translate(Vector3(0,0,0.0001))])
