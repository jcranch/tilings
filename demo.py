from periodic_tiling3 import cubic_tiling3
from matrix3 import rotate_x, rotate_y
from vector3 import Vector3
from restrict32 import restrict32
from tiling2_matplotlib import plot_matplotlib



def draw_cubic1_eps():

    def facecol((a, (r,g,b))):
        return (0.6 + (r%2)*0.2, 0.6 + (g%2)*0.2, 0.6 + (b%2)*0.2)

    m = rotate_x(0.75) * rotate_y(0.55)
    v = Vector3(0,0,-0.1)
    l3 = cubic_tiling3(((-6,6),(-6,6),(-6,6))).deform(m).translate(v)
    l2 = restrict32(l3).clip(-5,5,-5,5)
    with open("cubic1.eps", "w") as f:
        l2.write_eps(f, (20,220,520,720), (-5,5,-5,5), facecol=facecol)

    
def draw_cubic2_eps():

    def edgecol(((i,), t)):
        if i==1:
            return (0.3, 0.0, 0.0)
        elif i==2:
            return (0.0, 0.3, 0.0)
        elif i==3:
            return (0.0, 0.0, 0.3)
        else:
            raise ValueError("The edge should lie in some direction")

    l3 = cubic_tiling3(((-2,2),(-2,2),(-2,2))).translate(Vector3(0,0,3))
    with open("cubic2.eps", "w") as f:
        l3.write_eps(f, (0,0,500,500), (-1.5,5.7,-2.7,4.5),
                     whiterange=6, subdivs=25, edgecol=edgecol)


def draw_cubic1_matplotlib():

    m = rotate_x(0.75) * rotate_y(0.55)
    v = Vector3(0,0,-0.1)
    l3 = cubic_tiling3(((-6,6),(-6,6),(-6,6))).deform(m).translate(v)
    l2 = restrict32(l3)
    plot_matplotlib(l2).savefig("cubic1.png")

        
if __name__=="__main__":
    draw_cubic1_eps()
    draw_cubic2_eps()
    draw_cubic1_matplotlib()

