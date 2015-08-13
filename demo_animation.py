import sys

from vector4 import Vector4
from tiling4_polytope import *
from tiling3_polyhedron import *
from restrict43_animation import full_animation_43, translate_z, rotate_wx_transformation, uniform_rotate_transformation
from restrict32_animation import full_animation_32, rotate_z_transformation


def make_translate_z_4d(name, polytope):
    epsilon = Vector4(0,0,1e-9,1e-9)
    full_animation_43(tiling4 = polytope.translate(epsilon),
                      frames = int((polytope.maxz()-polytope.minz())*50)+2,
                      transformation_function = translate_z,
                      save_name = name)

def make_rotate_wx(name, polytope):
    epsilon = Vector4(1e-10,1e-11,1e-12,1e-13)
    full_animation_43(tiling4 = polytope.translate(epsilon),
                      frames = 180,
	              transformation_function = rotate_wx_transformation,
                      save_name = name)

def make_full_uniform_rotate_4d(name, polytope):
    epsilon = Vector4(1e-6,1e-7,1e-8,1e-9)
    full_animation_43(tiling4 = polytope.translate(epsilon),
                      frames = 180,
                      transformation_function = uniform_rotate_transformation,
                      save_name = name)

def make_rotate_z_3d(name, polytope):
    epsilon = Vector3(1e-6,1e-7,1e-8)
    full_animation_32(tiling3 = polytope.translate(epsilon),
                      frames = 180,
                      transformation_function = rotate_z_transformation,
                      save_name = name)

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
            make_rotate_wx(a, pentatope())
        elif a=="hypercube_full_uniform_rotate":
            make_rotate_wx(a, hypercube())
        elif a=="cell16_full_uniform_rotate":
            make_rotate_wx(a, cell16())
        elif a=="cell24_full_uniform_rotate":
            make_rotate_wx(a, cell24())
        elif a=="cell120_full_uniform_rotate":
            make_rotate_wx(a, cell120())
        elif a=="cell600_full_uniform_rotate":
            make_rotate_wx(a, cell600())
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
