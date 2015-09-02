from math import pi

from vector2 import Vector2
from vector3 import Vector3
from matrix3 import rotate_x, rotate_y, rotate_z
from tiling3_matplotlib import matplotlib_display_tiling3, matplotlib_display_tiling3_multiple
from tiling3_polyhedron import tetrahedron, octahedron, cube, icosahedron, dodecahedron
from tiling3_intersection_matplotlib import distribution_plot
from tiling2_matplotlib import plot_matplotlib_multiple
from tiling2_polygon import regular_polygon

if __name__=="__main__":
    plot_matplotlib_multiple([regular_polygon(i, grounded= True).translate(Vector2(i*2.5 -4,0)) for i in range(3,10)],
                         ticks_on = False, grid_on = False, userdefined_limits = [[2,20],[-2,2]])
    poster_polyhedra = {'tetrahedron': tetrahedron()
                                       .translate(Vector3(0,0,0.001))
                                       .deform(rotate_x(pi/9)*rotate_y(-6)*rotate_z(-pi/7))
                                       .scale(1.25),
                        'cube': cube()
                                .translate(Vector3(0,0,0.001))
                                .deform(rotate_x(pi/1)*rotate_y(pi/1)*rotate_z(-pi/1)),
                        'octahedron': octahedron()
                                      .translate(Vector3(0,0,0.001))
                                      .scale(1.25)
                                      .deform(rotate_x(-4.1)*rotate_y(-0.1)*rotate_z(2.2)),
                        'dodecahedron': dodecahedron()
                                        .translate(Vector3(0,0,0.001))
                                        .deform(rotate_x(0.3)*rotate_y(0)*rotate_z(0)),
                        'icosahedron': icosahedron()
                                       .translate(Vector3(0,0,0.001))
                                       .deform(rotate_x(0)*rotate_y(0.1)*rotate_z(0.25))}

    for platonic_solid in poster_polyhedra.itervalues():
        matplotlib_display_tiling3(tiling3 = platonic_solid)
        
    matplotlib_display_tiling3_multiple([polytope.translate(Vector3(0,0,0.000001)) for polytope in [cube(), octahedron()]], user_defined_axis_3D_limit = False)
    
    matplotlib_display_tiling3_multiple([dodecahedron().translate(Vector3(0,0,0.000001)).scale(2**0.5),
                                         icosahedron().translate(Vector3(0,0,0.000001))],
                                        user_defined_axis_3D_limit = False)
                                       
    matplotlib_display_tiling3_multiple([tetrahedron().translate(Vector3(0,0,0.000001)).scale(-1/3.0),
                                         tetrahedron().translate(Vector3(0,0,0.000001))],
                                       user_defined_axis_3D_limit = False)
