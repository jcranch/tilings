from vector3 import Vector3
from tiling3_matplotlib import matplotlib_display_tiling3
from tiling3_polyhedron import tetrahedron, octahedron, cube, icosahedron, dodecahedron
from tiling3_intersection_matplotlib import distribution_plot
from tiling2_matplotlib import plot_matplotlib_multiple


if __name__=="__main__":
    platonic_solids = [tetrahedron(), cube(), octahedron(), dodecahedron(), icosahedron()]
    for platonic_solid in platonic_solids:
        matplotlib_display_tiling3(tiling3 = platonic_solid.translate(Vector3(0,0,0.0001)))
        distribution_plot(platonic_solid)
    #First 6 regular polygon.
    plot_matplotlib_multiple([regular_polygon(i, grounded= True).translate(Vector2(i*2.5 -4,0)) for i in range(3,10)],
                         ticks_on = False, grid_on = False, userdefined_limits = [[2,20],[-2,2]] )
