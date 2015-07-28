"""
Exact arithmetic with the golden ratio: it shows up in a vast
number of constructions of polyhedra and polytopes.
"""

class GoldenInteger():

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return "%d + %d*tau"%(self.a, self.b)

    def __add__(self, other):
        if isinstance(other,int):
            return GoldenInteger(self.a + other, self.b)
        elif isinstance(other,GoldenInteger):
            return GoldenInteger(self.a + other.a, self.b + other.b)
        elif isinstance(other,float):
            return float(self)+other
        else:
            raise ValueError

    def __radd__(self, other):
        return self + other
        
    def __sub__(self, other):
        if isinstance(other,int):
            return GoldenInteger(self.a - other, self.b)
        elif isinstance(other,GoldenInteger):
            return GoldenInteger(self.a - other.a, self.b - other.b)
        elif isinstance(other,float):
            return float(self)-other
        else:
            raise ValueError

    def __rsub__(self, other):
        if isinstance(other,int):
            return GoldenInteger(other - self.a, -self.b)
        elif isinstance(other,float):
            return other-float(self)
        else:
            raise ValueError

    def __mul__(self, other):
        if isinstance(other,int):
            return GoldenInteger(self.a*other, self.b*other)
        elif isinstance(other,GoldenInteger):
            return GoldenInteger(self.a*other.a + self.b*other.b, self.a*other.b + self.b*other.a + self.b*other.b)
        elif isinstance(other,float):
            return float(self)*other
        else:
            raise ValueError

    def __rmul__(self, other):
        return self * other

    def __neg__(self):
        return GoldenInteger(-self.a, -self.b)
    
    def __float__(self):
        return self.a + self.b*(1 + 5**0.5)/2

    def __abs__(self):
        return abs(float(self))
    
    def conj(self):
        return GoldenInteger(self.a+self.b, -self.b)
    

tau = GoldenInteger(0,1)
