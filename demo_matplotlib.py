from vector3 import Vector3
from tiling3_matplotlib import matplotlib_display_tiling3
from tiling3_polyhedron import tetrahedron, octahedron, cube, icosahedron, dodecahedron
from tiling3_intersection_matplotlib import distribution_plot


if __name__=="__main__":
    platonic_solids = [tetrahedron(), cube(), octahedron(), dodecahedron(), icosahedron()]
    for platonic_solid in platonic_solids:
        matplotlib_display_tiling3(tiling3 = platonic_solid.translate(Vector3(0,0,0.0001)))
        distribution_plot(platonic_solid)
