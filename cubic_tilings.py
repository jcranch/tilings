from math import floor, ceil

from vector3 import Vector3
from tiling3 import Tiling3, big_union3



from itertools import product


class CubeFactory():
    """
    Some helper code for producing cubes and cubic tilings.
    """
    
    def dimension(self):
        raise NotImplemented
        
    def vector(self, a):
        raise NotImplemented

    def tiling(self):
        raise NotImplemented
    
    def __init__(self, dims=[[]]):
        self.n = self.dimension()
        self.data = [{} for i in xrange(self.n+1)]
        dims = [list(l) for l in dims]
        dims = [zip(l,l[1:]) for l in dims]
        for p in product(*dims):
            self.cube(self.n, tuple(tuple(a) for a in p))

    def faces(self, p):
        for (i,a) in enumerate(p):
            if len(a)==2:
                for v in a:
                    yield p[:i] + ((v,),) + p[i+1:]
            
    def cube(self, n, p):
        """
        An n-cube has 2n faces (of codimension 1), each formed by
        specialising one dimension.

        Given ((1,3),(2),(1,4)) it returns the 0, 1 and 2-dimensional
        structures of the rectangle [1,3] x {2} x [1,4].
        """        
        if p in self.data[n]:
            return self.data[n][p]
        if n==0:            
            a = self.vector(i for (i,) in p)
        else:
            a = frozenset(self.cube(n-1,p2) for p2 in self.faces(p))
        self.data[n][p] = a
        return a


class Cube3Factory(CubeFactory):

    def dimension(self):
        return 3
    
    def vector(self,(x,y,z)):
        return Vector3(x,y,z)

    def tiling(self):
        (v,e,f,g) = self.data
        v = dict((y,x) for (x,y) in v.iteritems())
        e = dict((y,x) for (x,y) in e.iteritems())
        f = dict((y,x) for (x,y) in f.iteritems())
        g = dict((y,x) for (x,y) in g.iteritems())
        return Tiling3(v,e,f,g)


def cube3(dims):
    """
    cube3([[x1,x2],[y1,y2],[z1,z2]]) is a Tiling3 representing a cube
    with dimensions as given.
    """
    return Cube3Factory(dims).tiling()
    

def cubic_tiling3(minx,maxx,miny,maxy,minz,maxz):
    """
    A Tiling3 representing an integer cubic lattice with given
    dimensions.
    """
    xs = xrange(int(floor(minx)), int(ceil(maxx))+1)
    ys = xrange(int(floor(miny)), int(ceil(maxy))+1)
    zs = xrange(int(floor(minz)), int(ceil(maxz))+1)
    return Cube3Factory([xs, ys, zs]).tiling()
