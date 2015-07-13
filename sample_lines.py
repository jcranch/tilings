from math import pi, floor, cos
from random import random
import Image

from matrix2 import rotation
from vector2 import Vector2
from restrict21 import restrict21


def sample_lines(polygon):
    bound = max(v.norm() for v in polygon.vertices)

    while True:
        angle = pi*random()
        m = rotation(angle)
        shift = (2*random()-1)*bound
        v = Vector2(0, shift)
        p = restrict21(polygon.transform(m).translate(v))
        s = frozenset(p.vertices[v] for e in p.edges for v in e)
        yield (angle, shift, s)
    


def plot(polygon, width, height, N=1000000):
    im = Image.new(mode="RGB", size=(width,height), color=(255,255,255))
    bound = max(v.norm() for v in polygon.vertices)

    def coords(x,y):
        return (int(floor(x * width / pi)),
                int(floor((y / bound / 2 + 0.5) * height)))
    
    n = 0
    for (a, s, l) in sample_lines(polygon):
        n += 1
        if n%10000 == 0:
            print str(n) + " "
        if n > N:
            break
            
        if l:
            if l == frozenset([(0,1), (2,0)]):
                col = (255,0,0)
            elif l == frozenset([(0,1), (1,2)]):
                col = (0,255,0)
            elif l == frozenset([(1,2), (2,0)]):
                col = (0,0,255)
            else:
                raise ValueError("Got unexpected label %s"%(l,))
            
            im.putpixel(coords(a,s),col)

    for n in xrange(3141):
        x = float(n)/1000.0
        im.putpixel(coords(x,-cos(x + pi/2) * bound), (0,0,0))
        im.putpixel(coords(x,-cos(x + 7*pi/6) * bound), (0,0,0))
        im.putpixel(coords(x,-cos(x + 11*pi/6) * bound), (0,0,0))

    return im
    

if __name__=="__main__":
    from tiling2_polygon import regular_polygon
    p = regular_polygon(3)
    im = plot(p, 400, 400)
    im.show()
    im.save("demos/moduli_lines.png")
