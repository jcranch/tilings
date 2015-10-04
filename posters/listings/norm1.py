z = Vector3(0,0,0)
v = dict((random_norm1(), None) for i in xrange(80))
e = dict((frozenset([x,z]), None) for x in v)
v[z] = None
t = Tiling3(v, e, {}, {})
