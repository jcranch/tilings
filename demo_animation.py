import sys

from vector4 import Vector4
from tiling4_polytope import *
from restrict43_animation import full_animation_43, translate_z


def make_translate_z(name, polytope):
    epsilon = Vector4(0,0,1e-9,1e-9)
    full_animation_43(tiling4 = polytope.translate(epsilon),
                      frames = int((polytope.maxz()-polytope.minz())*50)+2,
                      transformation_function = translate_z,
                      save_name = name)


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
        else:
            raise ValueError("Unrecognised argument: "+a)
