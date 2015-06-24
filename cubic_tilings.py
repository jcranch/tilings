from math import floor, ceil

from vector3 import Vector3
from tiling3 import Tiling3
from vector4 import Vector4
from tiling4 import Tiling4



from itertools import product


class CubeFactory():
    """
    Some helper code for producing cubes and cubic tilings.

    This class is intended to be subclassed: those subclasses should
    define the "dimension", "vector" and "tiling" methods.

    It is intended to be called with the coordinate choices. So, for
    example, calling it (in 2D) with argument [[1,2],[3,4]] will construct the
    square with coordinates (1,3), (1,4), (2,4) and (2,3).

    Calling it (in 3D) with arguments
    [xrange(11),xrange(11),xrange(11)] will construct a 10x10x10 array
    of cubes.
    """
    
    def dimension(self):
        "How many dimensions are we working in?"
        raise NotImplemented
        
    def vector(self, a):
        "Make a vector with coordinates a."
        raise NotImplemented

    def tiling(self):
        "Make a tiling of the appropriate sort using the data"
        raise NotImplemented
    
    def __init__(self, dims=[[]]):
        self.n = self.dimension()
        self.data = [{} for i in xrange(self.n+1)]
        dims = [list(l) for l in dims]
        dims = [zip(l,l[1:]) for l in dims]
        for p in product(*dims):
            self.cube(self.n, tuple(tuple(a) for a in p))

    def faces(self, p):
        """
        Given an n-cube, return its 2n faces of codimension 1, each
        formed by specialising one dimension.

        So, for example, the four faces of the square
        ((1, 2), (3, 4), (5,)) are
            ((1,), (3, 4), (5,))
            ((2,), (3, 4), (5,))
            ((1, 2), (3,), (5,))
            ((1, 2), (4,), (5,)).
        """
        for (i,a) in enumerate(p):
            if len(a)==2:
                for v in a:
                    yield p[:i] + ((v,),) + p[i+1:]
            
    def cube(self, n, p):
        """
        Ensure that the data corresponding to the cube with
        coordinates p is present. Works recursively, so is quite
        fast.
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


class Cube4Factory(CubeFactory):

    def dimension(self):
        return 4

    def vector(self,(w,x,y,z)):
        return Vector4(w,x,y,z)

    def tiling(self):
        (v,e,f,g,h) = self.data
        v = dict((y,x) for (x,y) in v.iteritems())
        e = dict((y,x) for (x,y) in e.iteritems())
        f = dict((y,x) for (x,y) in f.iteritems())
        g = dict((y,x) for (x,y) in g.iteritems())
        h = dict((y,x) for (x,y) in h.iteritems())
        return Tiling4(v,e,f,g,h)


def cube3(dims):
    """
    cube3([[x1,x2],[y1,y2],[z1,z2]]) is a Tiling3 representing a cube
    with dimensions as given.
    """
    return Cube3Factory(dims).tiling()
    

def cubic_tiling3(minx,maxx,miny,maxy,minz,maxz):
    """
    A Tiling3 representing the integer cubic lattice with given
    dimensions.
    """
    xs = xrange(int(floor(minx)), int(ceil(maxx))+1)
    ys = xrange(int(floor(miny)), int(ceil(maxy))+1)
    zs = xrange(int(floor(minz)), int(ceil(maxz))+1)
    return Cube3Factory([xs, ys, zs]).tiling()


def cube4(dims):
    """
    cube4([[w1,w2],[x1,x2],[y1,y2],[z1,z2]]) is a Tiling4 representing
    a cube with dimensions as given.
    """
    return Cube4Factory(dims).tiling()
    

def cubic_tiling4(minw,maxw,minx,maxx,miny,maxy,minz,maxz):
    """
    A Tiling4 representing the integer cubic lattice with given
    dimensions.
    """
    ws = xrange(int(floor(minw)), int(ceil(maxw))+1)
    xs = xrange(int(floor(minx)), int(ceil(maxx))+1)
    ys = xrange(int(floor(miny)), int(ceil(maxy))+1)
    zs = xrange(int(floor(minz)), int(ceil(maxz))+1)
    return Cube4Factory([ws, xs, ys, zs]).tiling()
