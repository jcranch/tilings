# %load demo_animation.py
import sys

from vector4 import Vector4
from vector3 import Vector3
from tiling4_polytope import *
from tiling3_polyhedron import *
from matrix4 import *
from matrix3 import *
from animation_matplotlib import tiling3_s_animation
from restrict43 import restrict43


def make_translate_z_4d(name, polytope, fpu=50.0, axis_limit=[[-2, 2]]*3, elevation=40, azimuth=30):
    minz = polytope.minz()
    maxz = polytope.maxz()
    tiling3_s_animation([[restrict43(polytope.translate(Vector4(0,0,0.00001,0.00001 + minz + i/fpu)))]
     for i in range(-1, int((maxz-minz)*fpu)+2)],
     folder='demos/'+name,
     axis_limit=axis_limit, elevation=elevation, azimuth=azimuth)

def make_rotate_wx(name, polytope, fpu=20.0, axis_limit=[[-2, 2]]*3, elevation_ = 40, azimuth_ = 30):
    tiling3_s_animation([[restrict43(polytope.deform(rotate_wx(i/fpu)).translate(Vector4(0,0,0.000001,0.000001)))]
     for i in range(int(2*pi*fpu)+1)], folder='demos/'+name,
     axis_limit=axis_limit, elevation=elevation, azimuth=azimuth)

def make_full_uniform_rotate(name, polytope, fpu=20.0, axis_limit=[[-2, 2]]*3, elevation=40, azimuth=30):
    tiling3_s_animation([[restrict43(polytope.deform(rotate_wx(i/fpu)*rotate_wy(i/fpu)*rotate_wz(i/fpu)*
                                                     rotate_xy(i/fpu)*rotate_xz(i/fpu)*rotate_yz(i/fpu))
                                                    .translate(Vector4(0,0,0.000001,0.000001)))]
     for i in range(int(2*pi*fpu)+1)], folder = 'demos/'+name,
     axis_limit=axis_limit, elevation=elevation, azimuth=azimuth)

def make_rotate_z_3d(name, polytope, fpu=20.0, axis_limit=[[-2, 2]]*3, elevation=40, azimuth=30):
    tiling3_s_animation([[polytope.deform(rotate_z(i/fpu)).translate(Vector3(0,0,0.000001))]
     for i in range(int(2*pi*fpu)+1)], folder='demos/'+name,
     axis_limit=axis_limit, elevation=elevation, azimuth=azimuth)

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
            make_translate_z_4d(a, cell120())
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
            make_rotate_wx(a, cell120())
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
            make_rotate_wx(a, cell120())
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
