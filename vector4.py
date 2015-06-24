from math import sqrt


class Vector4():

    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "Vector4(%f, %f, %f, %f)"%(self.w, self.x, self.y, self.z)
        
    def __hash__(self):
        return hash((Vector4, self.w, self.x, self.y, self.z))
        
    def __getitem__(self, n):
        if n == 1:
            return self.w
        elif n == 2:
            return self.x
        elif n == 3:
            return self.y
        elif n == 4:
            return self.z
        else:
            raise IndexError("Vector4 has components 1, 2, 3, 4 only.")

    def __add__(self, other):
        return Vector4(self.w + other.w, self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector4(self.w - other.w, self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, s):
        return Vector4(s*self.w, s*self.x, s*self.y, s*self.z)

    def __div__(self, s):
        return Vector4(self.w/s, self.x/s, self.y/s, self.z/s)

    def norm(self):
        return sqrt(self.w*self.w + self.x*self.x + self.y*self.y + self.z*self.z)
    
    def distance(self, other):
        return (self-other).norm()
