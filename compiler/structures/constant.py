class Constant:
    def __init__(self, address, name, type, value):
        self.address = -1
        self.name = name
        self.type = type
        self.value = value
    
    def address(self):
        return self.address
    
    def __str__(self) -> str:
        return 'Constant: ' + self.name + ', ' + self.type + ', ' + str(self.address())
