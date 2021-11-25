# -------------- variable.py --------------
# -- Rodrigo Bilbao -- Isabella Canales --
# 
# -- Lumos : Variable
# Object that represents a variable
# -----------------------------------------

class Variable:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.address = -1
        self.value = None
        self.dimensions = []
    
    def pushDimension(self, size):
        self.dimensions.append(size)

    def size(self):
        size = 1
        for d in self.dimensions:
            size *= d
        return size

    def __str__(self) -> str:
        return "[" + self.name + " " + str(self.type) + " " + str(self.address) + "]"