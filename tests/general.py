from vector2 import Vector2
from vector3 import Vector3



class TilingTest():

    def type_tiling2(self, t):
        """
        Check that a 2D tiling is made of the things it is supposed to.
        """
        self.assertIsInstance(t.vertices, dict, "vertices should form a dict")
        for v in t.vertices:
            self.assertIsInstance(v, Vector2, "vertices should be 2-vectors")
        self.assertIsInstance(t.edges, dict, "edges should form a dict")
        for e in t.edges:
            self.assertIsInstance(e, frozenset, "edges should be frozensets")
            for v in e:
                self.assertIsInstance(v, Vector2, "edges should be made up of vertices")
        self.assertIsInstance(t.faces, dict, "faces should form a dict")
        for f in t.faces:
            self.assertIsInstance(f, frozenset, "faces should be frozensets")
            for e in f:
                self.assertIsInstance(e, frozenset, "faces should be made up of frozensets")
                for v in e:
                    self.assertIsInstance(v, Vector2, "faces should be made up of frozensets made up of vertices")

    def type_tiling3(self, t):
        """
        Check that a 3D tiling is made of the things it is supposed to.
        """
        self.assertIsInstance(t.vertices, dict, "vertices should form a dict")
        for v in t.vertices:
            self.assertIsInstance(v, Vector3, "vertices should be 3-vectors")
        self.assertIsInstance(t.edges, dict, "edges should form a dict")
        for e in t.edges:
            self.assertIsInstance(e, frozenset, "edges should be frozensets")
            for v in e:
                self.assertIsInstance(v, Vector3, "edges should be made up of vertices")
        self.assertIsInstance(t.faces, dict, "faces should form a dict")
        for f in t.faces:
            self.assertIsInstance(f, frozenset, "faces should be frozensets")
            for e in f:
                self.assertIsInstance(e, frozenset, "faces should be made up of frozensets")
                for v in e:
                    self.assertIsInstance(v, Vector3, "faces should be made up of frozensets made up of vertices")
        self.assertIsInstance(t.volumes, dict, "volumes should form a dict")
        for g in t.volumes:
            self.assertIsInstance(g, frozenset, "volumes should be frozensets")
            for f in g:
                self.assertIsInstance(f, frozenset, "volumes should be made up of frozensets")
                for e in f:
                    self.assertIsInstance(e, frozenset, "volumes should be made up of frozensets made up of frozensets")
                    for v in e:
                        self.assertIsInstance(v, Vector3, "volumes should be made up of frozensets made up of frozensets made up of vertices")
