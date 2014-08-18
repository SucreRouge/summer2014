

#Simple vector class to allow for vector addition and scalar multiplication
class Vector:
    def __init__(self, vals):
        self.data = list(vals)
    
    def __repr__(self):
        return self.data.__repr__()

    def __getitem__(self, idx):
        return self.data[idx]
    def __add__(self, other):
        return Vector([x + y for (x, y) in zip(self.data, other.data)])
    def __rmul__(self, val):
        return Vector([val*x for x in self.data])
    def __neg__(self):
        return Vector([-x for x in self.data])
    def __sub__(self, other):
        return self.__add__(-other)
    def __len__(self):
        return len(self.data)
