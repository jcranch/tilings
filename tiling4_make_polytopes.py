import os
import sys

from common import remove_duplicates
from permutations import *
from tau import tau,root5
from tiling4_polytope import tiling4_convex_hull
from vector4 import Vector4


def cell24():
    '''
    The 24 Cell.
    '''
    def vertices():
        for p in all_permutations_plus_minus([2,0,0,0]):
            yield p
        for p in all_permutations_plus_minus([1,1,1,1]):
            yield p

    vs = (Vector4(w,x,y,z) for (w,x,y,z) in remove_duplicates(vertices()))
    return tiling4_convex_hull(dict(zip(vs,xrange(24))),
                               statusreport=True,
                               max_volumes_per_vertex=6)

def cell120():
    '''
    The 120 Cell.
    '''
    tau2 = tau*tau
    taui = -tau.conj()
    tau2i = taui*taui

    def vertices():
        for p in all_permutations_plus_minus([2,2,0,0]):
            yield p
        for p in all_permutations_plus_minus([1,1,1,root5]):
            yield p
        for p in all_permutations_plus_minus([tau,tau,tau,tau2i]):
            yield p
        for p in all_permutations_plus_minus([taui,taui,taui,tau2]):
            yield p
        for p in even_permutations_plus_minus([0,tau2i,1,tau2]):
            yield p
        for p in even_permutations_plus_minus([0,taui,tau,root5]):
            yield p
        for p in even_permutations_plus_minus([taui,1,tau,2]):
            yield p

    vs = (Vector4(w,x,y,z) for (w,x,y,z) in remove_duplicates(vertices()))

    return tiling4_convex_hull(dict(zip(vs,xrange(600))),
                               statusreport=True,
                               max_volumes_per_vertex=4)

def cell600():
    '''
    The 600 Cell.
    '''
    def vertices():
        for p in all_permutations_plus_minus([1,1,1,1]):
            yield p
        for p in all_permutations_plus_minus([0,0,0,2]):
            yield p
        for p in even_permutations_plus_minus([tau,1,tau.conj(),0]):
            yield p

    vs = (Vector4(w,x,y,z) for (w,x,y,z) in remove_duplicates(vertices()))

    return tiling4_convex_hull(dict(zip(vs,xrange(120))), statusreport=True)


if __name__=="__main__":

    if not os.path.exists("autotilings"):
        os.makedirs("autotilings")

    if len(sys.argv) < 2:
        raise ValueError("No arguments supplied")

    for v in sys.argv[1:]:

        if v == "cell24":
            print "cell24:"
            c = cell24()
            with open("autotilings/cell24.data", 'w') as f:
                f.write(repr(c))

        elif v == "cell120":
            print "cell120:"
            c = cell120()
            with open("autotilings/cell120.data", 'w') as f:
                f.write(repr(c))

        elif v == "cell600":
            print "cell600:"
            c = cell600()
            with open("autotilings/cell600.data", 'w') as f:
                f.write(repr(c))
                
        else:
            raise ValueError("Argument unrecognised: " + v)
