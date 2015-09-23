from matplotlib_imagemaker import Tiling2ImageMaker, Tiling3ImageMaker
from tiling2_polygon import regular_polygon
from tiling3_polyhedron import *
from tiling4_polytope import *
from vector2 import Vector2
from vector3 import Vector3
from vector4 import Vector4
from matrix2 import rotation
from matrix3 import *
from matrix4 import *
from restrict43 import restrict43
from tiling2_periodic import *
from tiling4_periodic import cell24_tiling

from math import pi
import matplotlib.pyplot as plt

if __name__=="__main__":
    poster_figure = plt.figure(figsize = [10,2])
    b = Tiling3ImageMaker()
    b.number_of_rows = 1
    b.number_of_columns = 5
    b.tiling3_axis_limit = [[-1.2,1.2]]*3
    b.figure_size = [10,2]
    
    b.position_code = 1
    b.azimuth = -25
    b.elevation = -40
    b.image([tetrahedron()])
    
    b.position_code = 2
    b.azimuth = 31
    b.elevation = 26
    b.image([cube()])
    
    b.position_code = 3
    b.azimuth = -13
    b.elevation = 13
    b.image([octahedron().scale(1.5)])
    
    b.position_code = 4
    b.azimuth = 18
    b.elevation = 30
    b.image([dodecahedron()])
    
    b.position_code = 5
    b.azimuth = 45
    b.elevation = 31
    b.image([icosahedron()])
    
    plt.savefig('posters/diagrams/platonic_solids')
    plt.close()
    
    poster_figure = plt.figure(figsize = [10,2])
    b = Tiling3ImageMaker()
    b.number_of_rows = 1
    b.number_of_columns = 5
    b.tiling3_axis_limit = [[-1.2,1.2]]*3
    b.tiling3_faces_on = False
    b.edge_colours = ['black', 'blue']
    b.edges_alpha = 0.4
    
    b.position_code = 1
    b.elevation = 19
    b.azimuth = -94
    b.image([tiling3_dual(tetrahedron()), tetrahedron()])
    
    b.position_code = 2
    b.elevation = 17
    b.azimuth = 22
    b.image([tiling3_dual(cube()), cube()])
    
    b.position_code = 3
    b.elevation = 10
    b.azimuth = 24
    b.image([tiling3_dual(octahedron().scale(1.5)), octahedron().scale(1.5)])
    
    b.position_code = 4
    b.elevation = 29
    b.azimuth = 9
    b.image([tiling3_dual(dodecahedron()), dodecahedron()])
    
    b.position_code = 5
    b.elevation = 31
    b.azimuth = 45
    b.image([tiling3_dual(icosahedron()), icosahedron()])
    
    plt.savefig('posters/diagrams/dual_platonic_solids')
    plt.close()
    
    poster_figure = plt.figure(figsize = [10,2])
    b = Tiling2ImageMaker()
    b.number_of_rows = 1
    b.number_of_columns = 5
    b.tiling2_axis_limit =  [[-1,1]]*2 
    for n in range(3,8):
        b.position_code = n-2
        b.image([regular_polygon(n)])
        
    plt.savefig('posters/diagrams/regular_polygons')
    plt.close()
    
    poster_figure = plt.figure(figsize = [10,4])
    
    polytope = cube()
    
    minz = polytope.minz()
    maxz = polytope.maxz()
    a = [-1,1,2,3,5]
    b = Tiling3ImageMaker()
    b.tiling3_faces_on = False
    b.restrict32_intersection_on = True
    b.azimuth = -35
    b.elevation = 15
    b.edges_alpha = 0.3
    b.number_of_columns = 5
    b.plane_z0_on = True
    b.tiling2_alpha = 0.8
    
    b.tiling3_axis_limit = [[-1.7,1.7]]*3
    for (j,i) in enumerate(a):
        b.position_code = j+1
        b.image([polytope.translate(Vector3(0,0,-0.00001 + minz + i/2.0))])
                         
    plt.savefig('posters/diagrams/cube_slice_1')
    plt.close()
    
    poster_figure = plt.figure(figsize = [12,4])
    
    polytopes = [cube().deform(rotation_matrix_producer(Vector3(3,6,5)))]
    subplot_count = 0
    a = range(11)
    b = Tiling3ImageMaker()
    b.tiling3_faces_on = False
    b.restrict32_intersection_on = True
    b.azimuth = 119
    b.elevation = -27
    b.edges_alpha = 0.3
    b.number_of_rows = 2
    b.number_of_columns = 6
    b.plane_z0_on = True
    b.tiling2_alpha = 0.8
    b.tiling3_axis_limit = [[-1.8,1.8]]*3
    
    for polytope in polytopes:
        minz = polytope.minz()
        maxz = polytope.maxz()
        rate = float(abs(maxz-minz))/(len(a))
        for i in a+[len(a)]:
            b.position_code = (i+1)
            b.image([polytope.translate(Vector3(0,0.00001,-0.001 + minz + i*rate))])
            
    
    plt.savefig('posters/diagrams/cube_slice_2')
    plt.close()
    
    poster_figure = plt.figure(figsize = [40,4])
    
    polytopes = [cell600(), cell120()]
    subplot_count = 0
    b = Tiling3ImageMaker()
    b.elevation = 31
    b.azimuth = -147
    b.edges_alpha = 0.15
    b.number_of_rows = 2
    b.number_of_columns = 16
    for (j,polytope) in enumerate(polytopes):
        minz = polytope.minz()
        maxz = polytope.maxz()
        b.tiling3_axis_limit = [[-1.2,1.2]]*3
        if j == 1:
            b.elevation = -3
            b.azimuth = -143
            b.tiling3_axis_limit = [[-1.7,1.7]]*3
        a = range(16)
        rate = float(abs(maxz-minz))/(len(a))
        for i in a:
            b.image([restrict43(polytope.translate(Vector4(0,0,0.00001,-0.001 + minz + i*rate)))])
            b.position_code = (i+1)+subplot_count*(len(a))
        subplot_count += 1
    
    plt.savefig('posters/diagrams/cell600_cell120')
    plt.close()
    
    poster_figure = plt.figure(figsize = [30,4])
    
    polytopes = [hypercube(), hypercube().deform(rotate_wx(pi/3)*rotate_wz(5*pi/4)*rotate_yz(3*pi/5))]
    subplot_count = 0
    b = Tiling3ImageMaker()
    b.elevation = 20
    b.azimuth = 20
    b.edges_alpha = 0.15
    b.number_of_rows = 2
    
    for (j,polytope) in enumerate(polytopes):
        minz = polytope.minz()
        maxz = polytope.maxz()
        b.tiling3_axis_limit = [[-1.2,1.2]]*3
        if j == 1:
            b.tiling3_axis_limit = [[-1.2,1.2]]*3
        a = range(15)
        b.number_of_columns = len(a)
        rate = float(abs(maxz-minz))/(len(a))
        for i in a:
            b.image([restrict43(polytope.translate(Vector4(0,0,0.00001,-0.001 + minz + i*rate)))])
            b.position_code = (i+1)+subplot_count*(len(a))
        subplot_count += 1
        b.elevation = 16
        b.azimuth = -117
    
    plt.savefig('posters/diagrams/hypercube')
    plt.close()
    
    lattices = [cubic_tiling2([[-10,10]]*2).translate(Vector2(0.2,0.3)).deform(rotation(pi/8)), 
                triangular_tiling([[-10,10]]*2).deform(rotation(-pi/8)),
                hexagonal_tiling([[-10,10]]*2).deform(rotation(pi/8))]
    
    
    poster_figure = plt.figure(figsize = [4,10])
    b = Tiling2ImageMaker()
    b.number_of_rows = 3
    b.number_of_columns = 1
    
    
    for i in range(len(lattices)):
        if i == 0:
            b.tiling2_axis_limit = [[-2,2]]*2
        if i == 1:
            b.tiling2_axis_limit = [[-1,2]]*2
        if i == 2:
            b.tiling2_axis_limit = [[-3,3]]*2
        b.position_code = i+1
        b.image([lattices[i]])
    
        
    plt.savefig('posters/diagrams/tessalations_2d')
    plt.close()
    m010_1 =\
    Matrix4([[0.056328, -0.675362, -0.290862,0.675362], 
             [-0.624211, -0.184595, 0.736349,0.184595], 
             [0.779222, -0.099053, 0.610893,0.099053],
             [0.000000, -0.707107, 0.000000,-0.707107]])
    m010_1
    m011_1 =\
    Matrix4([[-0.071790, -0.165030, 0.773165,0.608135],
                      [0.978870, -0.165143, 0.103850,-0.061292],
                      [-0.191468, -0.782406, 0.241036,-0.541371],
                      [0.000000, 0.577350, 0.577350,-0.577350]])
    
    poster_figure = plt.figure(figsize = [12,9])
    
    b=Tiling3ImageMaker()
    b.number_of_rows = 3
    b.number_of_columns = 4
    
    
    for i in range(12):
        b.position_code = i + 1
        if i == 0:
            b.tiling3_axis_limit = [[-1.5,1.5]]*3
            b.azimuth = 82
            b.elevation = 27
            a = cell24_tiling([[-3,3],[-3,3],[-3,3],[-3,3]])
        if i == 1:
            b.tiling3_axis_limit = [[-1,3]]*3
            b.azimuth = 4
            b.elevation = 19
            a = cell24_tiling([[-5,3],[-3,5],[-3,3],[-3,3]]).translate(Vector4(-2,0,0,0))
        if i == 2:
            b.tiling3_axis_limit = [[-1,3]]*3
            b.azimuth = 29
            b.elevation = 7
            a = cell24_tiling([[-5,3],[-5,3],[-3,5],[-5,5]]).translate(Vector4(-2,0,0,0)) 
        if i == 3:
            b.tiling3_axis_limit = [[-2,4]]*3
            b.azimuth = 22
            b.elevation = -1
            a = cell24_tiling([[-5,5],[-5,5],[-5,5],[-5,5]]).translate(Vector4(-2,0,0,0))         
        b.image([restrict43((a.translate(Vector4(0,0,0.00001,0.00001))))])
        if i == 4:
            b.tiling3_axis_limit = [[-1.5,1.5]]*3
            b.azimuth = -30
            b.elevation = 38
            a = cell24_tiling([[-3,3],[-3,3],[-3,3],[-3,3]]).deform(m010_1)
        if i == 5:
            b.tiling3_axis_limit = [[-1,3]]*3
            b.azimuth = -35
            b.elevation = -138
            a = cell24_tiling([[-5,3],[-5,3],[-3,5],[-5,3]]).translate(Vector4(0,0,0,0)).deform(m010_1)
        if i == 6:
            b.tiling3_axis_limit = [[-2.2,2.5]]*3
            b.azimuth = 71
            b.elevation = -153
            a = cell24_tiling([[-5,3],[-5,3],[-3,5],[-5,5]]).translate(Vector4(0,0,0,0)).deform(m010_1)
        if i == 7:
            b.tiling3_axis_limit = [[-4,4]]*3
            b.azimuth = 69
            b.elevation = 36
            a = cell24_tiling([[-5,5],[-5,5],[-5,5],[-5,5]]).translate(Vector4(0,0,0,0)).deform(m010_1)    
        b.image([restrict43(a.translate(Vector4(0,0,0.00001,0.00001)))])
        if i == 8:
            b.tiling3_axis_limit = [[-1.5,1.5]]*3
            b.azimuth = -47
            b.elevation = 172
            a = cell24_tiling([[-3,3],[-3,3],[-3,3],[-3,3]]).deform(m011_1)
        if i == 9:
            b.tiling3_axis_limit = [[-2,2]]*3
            b.azimuth = 43
            b.elevation = -55
            a = cell24_tiling([[-5,3],[-3,5],[-3,3],[-3,3]]).translate(Vector4(2,0,0,0)).deform(m011_1)
        if i == 10:
            b.tiling3_axis_limit = [[-2.2,2.5]]*3
            b.azimuth = -58
            b.elevation = 46
            a = cell24_tiling([[-5,3],[-5,3],[-3,5],[-5,5]]).translate(Vector4(0,0,0,0)).deform(m011_1)
        if i == 11:
            b.tiling3_axis_limit = [[-4,4]]*3
            b.azimuth = 69
            b.elevation = 33
            a = cell24_tiling([[-5,5],[-5,5],[-5,5],[-5,5]]).translate(Vector4(0,0,0,0)).deform(m011_1)    
        b.image([restrict43(a.translate(Vector4(0,0,0.00001,0.00001)))])
    
    plt.savefig('posters/diagrams/cell24')
    plt.close()


