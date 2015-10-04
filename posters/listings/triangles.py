def triangular_tiling(bounding_box):
    periods = [Vector2(1, 0), Vector2(0.5, 3**0.5/2)]
    fundamental_vertex = {(): Vector2(0, 0)}
    fundamental_edges = {(1,): [((), (0, 0)), ((), (0, 1))], # /
                         (2,): [((), (0, 0)), ((), (1, 0))], # -
                         (3,): [((), (0, 1)), ((), (1, 0))]} # \
    fundamental_faces = {True:  [((1,), (0, 0)),
                                 ((2,), (0, 0)),
                                 ((3,), (0, 0))],
                         False: [((1,), (1, 0)),
                                 ((2,), (0, 1)),
                                 ((3,), (0, 0))]}
    return periodic_tiling2(fundamental_vertex,
                            fundamental_edges,
                            fundamental_faces,
                            bounding_box, periods)
