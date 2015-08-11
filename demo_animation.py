import sys

from vector4 import Vector4
from tiling4_polytope import *
from restrict43_animation import full_animation_43, translate_z, rotate_wx_transformation


def make_translate_z(name, polytope):
    epsilon = Vector4(0,0,1e-9,1e-9)
    full_animation_43(tiling4 = polytope.translate(epsilon),
                      frames = int((polytope.maxz()-polytope.minz())*50)+2,
                      transformation_function = translate_z,
                      save_name = name)

def make_rotate_wx(name, polytope):
    full_animation_43(tiling4 = regular_polytopes[polytope].translate(Vector4(0,0,0.000000001,0.0000000001)),
                      frames = 180,
	              transformation_function = rotate_wx_transformation,
                      save_name = polytope +'_rotate_wx')

if __name__=="__main__":
    for a in sys.argv[1:]:
        if a=="pentatope_translate_z":
            make_translate_z(a, pentatope())
        elif a=="hypercube_translate_z":
            make_translate_z(a, hypercube())
        elif a=="cell16_translate_z":
            make_translate_z(a, cell16())
        elif a=="cell24_translate_z":
            make_translate_z(a, cell24())
        elif a=="cell120_translate_z":
            make_translate_z(a, cell120())
        elif a=="cell600_translate_z":
            make_translate_z(a, cell600())
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
        else:
            raise ValueError("Unrecognised argument: "+a)
