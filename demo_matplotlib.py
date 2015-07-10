from vector3 import Vector3
from tiling3_matplotlib import matplotlib_display_tiling3
from tiling3_polyhedron import tetrahedron, octahedron


if __name__=="__main__":
    matplotlib_display_tiling3(tiling3 = tetrahedron().translate(Vector3(0,0,0.00000001)))
    matplotlib_display_tiling3(tiling3 = octahedron().translate(Vector3(0,0,0.00000001)))
