import os
import random
import sys

from vector3 import Vector3, random_norm1
from tiling3 import Tiling3

target_dir = "posters/codeimages"


def unit_ball():

    random.seed("A seed to keep the pattern consistent.")
    z = Vector3(0,0,0)
    v = dict((random_norm1(), None) for i in xrange(80))
    e = dict((frozenset([x,z]), None) for x in v)
    v[z] = None
    t = Tiling3(v, e, {}, {}).translate(Vector3(0,0,2))

    with open(os.path.join(target_dir, "unit_ball.eps"), 'w') as f:
        geobox = (0.1, 2.8, -0.6, 1.8)
        psbox = (0, 0, 200, 200)
        edgecol = lambda x: random.choice([(1,0,0), (0,1,0), (0,0,1)])
        t.write_eps(f, psbox, geobox, edgecol=edgecol, whiterange=3.0)


if __name__=="__main__":
    a = sys.argv[1:]
    if not a:
        print "Run with the names of the files to generate"
        exit()
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    for n in a:
        n = n.split("/")[-1].split(".")[0]
        if n=="unit_ball":
            unit_ball()
