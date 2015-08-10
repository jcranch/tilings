from tiling4_polytope import regular_polytopes_4d 
from restrict43_animation import full_animation_43, translate_z

if __name__=="__main__":
    for polytope in regular_polytopes_4d:
        full_animation_43(tiling4 = regular_polytopes[polytope].translate(Vector4(0,0,0.000000001,0.0000000001)),
                          frames = int(regular_polytopes[polytope].maxz() - regular_polytopes[polytope].minz())*50+2,
                          transformation_function = translate_z, 
                          save_name = polytope +'_translate_z')
