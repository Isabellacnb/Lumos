class QuadrupleList():
    def __init__(self):
        self.quads = []
    
    def push(self, quad):
        print("ADDED ", str(quad))
        self.quads.append(quad)
    
    def at(self, ind):
        return self.quads[ind]

    def empty(self):
        return len(self.quads) == 0

    def clear(self):
        self.quads.clear()
    
    def size(self):
        return len(self.quads)
    
    def __str__(self) -> str:
        string = ""

        for idx, quad in enumerate(self.quads):
            string += str(idx) + ") " + str(quad) + "\n"
        
        return string[:-1]
