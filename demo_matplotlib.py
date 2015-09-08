from math import pi

from vector2 import Vector2
from vector3 import Vector3
from matrix3 import rotate_x, rotate_y, rotate_z
from tiling3_matplotlib import tiling3_s_3d_subplot
from tiling3_polyhedron import tetrahedron, octahedron, cube, icosahedron, dodecahedron
from tiling3_intersection_matplotlib import distribution_plot
from tiling2_matplotlib import plot_matplotlib_multiple
from tiling2_polygon import regular_polygon


if __name__=="__main__":
    platonic_solids = [tetrahedron(), cube(), octahedron(), dodecahedron(), icosahedron()]
    for platonic_solid in platonic_solids:
        tiling3_s_3d_subplot([platonic_solid.translate(Vector3(0,0,0.0001))])
        distribution_plot(platonic_solid)
