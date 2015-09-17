import sys

from vector4 import Vector4
from vector3 import Vector3
from tiling4_polytope import *
from tiling3_polyhedron import *
from matrix4 import *
from matrix3 import *
from matplotlib_imagemaker import Tiling3ImageMaker
from restrict43 import restrict43


def make_translate_z_4d(name, polytope,frames = 500,axis_limit=[[-1.2, 1.2]]*3, elevation=40, azimuth=30):
    b = Tiling3ImageMaker()
    minz = polytope.minz()
    maxz = polytope.maxz()
    b.tiling3_axis_limit = axis_limit
    b.elevation = elevation
    b.azumith = azimuth
    a = range(frames+1)
    rate = abs(maxz-minz)/(len(a))
    b.animation([[restrict43(polytope.translate(Vector4(0,0,0.00001,-0.001 + minz + i*rate)))] for i in a],'demos/'+name)
    return None

def make_rotate_wx(name, polytope, frames = 500, axis_limit=[[-1.2, 1.2]]*3, elevation = 40, azimuth = 30):
    b = Tiling3ImageMaker()
    b.tiling3_axis_limit = axis_limit
    b.elevation = elevation
    b.azumith = azimuth
    rate = (2*pi)/frames
    a = range(frames+1)
    b.animation([[restrict43(polytope.deform(rotate_wx(i*rate)).translate(Vector4(0,0,0.000001,0.000001)))]
     for i in a], 'demos/'+name)
def make_full_uniform_rotate(name, polytope, frames = 500, axis_limit=[[-2, 2]]*3, elevation=40, azimuth=30):
    b = Tiling3ImageMaker()
    b.tiling3_axis_limit = axis_limit
    b.elevation = elevation
    b.azumith = azimuth
    rate = (2*pi)/frames
    a = range(frames+1)
    b.animation([[restrict43(polytope.deform(rotate_wx(i*rate)*rotate_wy(i*rate)*rotate_wz(i*rate)*
                                             rotate_xy(i*rate)*rotate_xz(i*rate)*rotate_yz(i*rate))
                             .translate(Vector4(0,0,0.000001,0.000001)))]
     for i in a], 'demos/'+name)
    
def make_rotate_z(name, polytope, frames = 50, axis_limit=[[-1.2, 1.2]]*3, elevation = 40, azimuth = 30):
    b = Tiling3ImageMaker()
    b.tiling3_axis_limit = axis_limit
    b.elevation = elevation
    b.azumith = azimuth
    rate = (2*pi)/frames
    a = range(frames+1)
    b.animation([[polytope.deform(rotate_z(i*rate)).translate(Vector3(0,0,0.000001,))]
     for i in a], 'demos/'+name)
     
if __name__=="__main__":
    for a in sys.argv[1:]:
        if a=="pentatope_translate_z":
            make_translate_z_4d(a, pentatope())
        elif a=="hypercube_translate_z":
            make_translate_z_4d(a, hypercube())
        elif a=="cell16_translate_z":
            make_translate_z_4d(a, cell16())
        elif a=="cell24_translate_z":
            make_translate_z_4d(a, cell24())
        elif a=="cell120_translate_z":
            make_translate_z_4d(a, cell120(), axis_limit=[[-2.2, 2.2]]*3)
        elif a=="cell600_translate_z":
            make_translate_z_4d(a, cell600())
        elif a=="pentatope_rotate_wx":
            make_rotate_wx(a, pentatope())
        elif a=="hypercube_rotate_wx":
            make_rotate_wx(a, hypercube())
        elif a=="cell16_rotate_wx":
            make_rotate_wx(a, cell16())
        elif a=="cell24_rotate_wx":
            make_rotate_wx(a, cell24())
        elif a=="cell120_rotate_wx":
            make_rotate_wx(a, cell120(), axis_limit=[[-2.2, 2.2]]*3)
        elif a=="cell600_rotate_wx":
            make_rotate_wx(a, cell600())
        elif a=="pentatope_full_uniform_rotate":
            make_full_uniform_rotate(a, pentatope())
        elif a=="hypercube_full_uniform_rotate":
            make_full_uniform_rotate(a, hypercube())
        elif a=="cell16_full_uniform_rotate":
            make_full_uniform_rotate(a, cell16())
        elif a=="cell24_full_uniform_rotate":
            make_full_uniform_rotate(a, cell24())
        elif a=="cell120_full_uniform_rotate":
            make_rotate_wx(a, cell120(), axis_limit=[[-2.2, 2.2]]*3)
        elif a=="cell600_full_uniform_rotate":
            make_full_uniform_rotate(a, cell600())
        elif a=="tetrahedron_rotate_z":
            make_rotate_z_3d(a, tetrahedron())
        elif a=="cube_rotate_z":
            make_rotate_z_3d(a, cube())
        elif a=="octahedron_rotate_z":
            make_rotate_z_3d(a, octahedron())
        elif a=="icosahedron_rotate_z":
            make_rotate_z_3d(a, icosahedron())
        elif a=="dodecahedron_rotate_z":
            make_rotate_z_3d(a, dodecahedron())
        else:
            raise ValueError("Unrecognised argument: "+a)
