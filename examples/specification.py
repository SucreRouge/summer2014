#file: specification.py
import math

class Specification:
    def __init__(self):
        pass
    #Evaluate a vector to produce a value in the ordering
    def worth(self,vec):
        pass

class Lexicographic(Specification):
    #Impose lexicographic ordering on a bunch of specs
    def __init__(self, *specs):
        self.specs = specs
    def worth(self, vec):
        return tuple(spec.worth(vec) for spec in self.specs)

class ID(Specification):
    #Reference the kth identifier
    def __init__(self, k):
        self.k = k
    def worth(self, vec):
        return vec[self.k]

class Number(Specification):
    #Constant
    def __init__(self, n):
        self.n = n
    def worth(self, vec):
        return self.n

class Negate(Specification):
    #Negate the value
    def __init__(self, spec):
        self.spec = spec
    def worth(self, vec):
        return -self.spec.worth(vec)

class Binop(Specification):
    #Binary operation on specifications
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Add(Binop):
    #Add two specifications
    def worth(self, vec):
        return self.left.worth(vec) + self.right.worth(vec)

class Mult(Binop):
    #Multiply two specifications
    def worth(self, vec):
        return self.left.worth(vec) * self.right.worth(vec)

class Gte(Binop):
    #Greater than or equal to specification
    def worth(self, vec):
        if self.left.worth(vec) >= self.right.worth(vec):
            return 0
        else:
            lw = self.left.worth(vec)
            rw = self.right.worth(vec)
            return -abs(lw - rw)/math.sqrt(2) #distance to lw > rw

class Gt(Binop):
    #Greater than
    def worth(self, vec):
        if self.left.worth(vec) > self.right.worth(vec):
            return 0
        else:
            lw = self.left.worth(vec)
            rw = self.right.worth(vec)
            return -abs(lw - rw)/math.sqrt(2) - .1
            
