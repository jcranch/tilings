from math import floor, ceil

from vector3 import Vector3
from tiling3 import Tiling3, big_union3
#Just a few questions to clarify some confusion. Demo runs well on my laptop !


class CubeFactory():
    """
    Just some helper code producing cubes.
    """

    def vector(self,a):
        raise NotImplemented

    def inner(self,n,a):
        """
        An n-cube has 2n faces (of codimension 1), each formed by      # I'm unfamiliar with this notation for a rectangle.
        specialising one dimension.                                  
                                                                       # This is my interpretation (I suspect it is wrong) :    
        Given [[1,3],[2],[1,4]] it returns the 0, 1 and 2-dimensional  # This is describing the rectange with vertices (1,3),(1,4),(3,3),(3,4)
        structures of the rectangle [1,3] x {2} x [1,4].               # As we start with the 0-dimensional point (1,3) and create a one-dimensional edge of length 2 from (1,3) to (3,3) 
        """                                                            # And we create lines (1,y) to (3,y) for all y in [3,4] to create our 2d rectangle.
        if n==0:
            return [{self.vector([i for (i,) in a]):tuple(tuple(x) for x in a)}] # Please can you give an example of a as I'm struggling to interpret this line. Is this the same sort of a we would use in the vector method?
        else:
            data = [{} for i in xrange(n)]
            for i in xrange(len(a)):
                if len(a[i])==2:
                    for v in a[i]:
                        data2 = self.inner(n-1, a[:i] + [[v]] + a[i+1:])
                        for (d,d2) in zip(data,data2):
                            d.update(d2.iteritems())
            data.append({frozenset(data[-1]):tuple(tuple(x) for x in a)})
            return data
    
    def data(self,dims):
        return self.inner(len(dims), dims)


class Cube3Factory(CubeFactory):

    def vector(self,(x,y,z)):
        return Vector3(x,y,z)
    

def cube3(dims):
    """
    cube3([[x1,x2],[y1,y2],[z1,z2]]) is a cube with dimensions as given.
    """
    (v,e,f,g) = Cube3Factory().data(dims)
    return Tiling3(v,e,f,g)
    

def cubic_tiling3(minx,maxx,miny,maxy,minz,maxz):
    """
    A Tiling3 representing a cubic tiling.
    """
    minx = int(floor(minx))
    maxx = int(ceil(maxx))
    miny = int(floor(miny))
    maxy = int(ceil(maxy))
    minz = int(floor(minz))
    maxz = int(ceil(maxz))

    return big_union3(cube3([[x,x+1],[y,y+1],[z,z+1]])
                      for x in xrange(minx,maxx)
                      for y in xrange(miny,maxy)
                      for z in xrange(minz,maxz))
