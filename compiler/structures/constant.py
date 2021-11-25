# -------------- constant.py --------------
# -- Rodrigo Bilbao -- Isabella Canales --
# 
# -- Lumos : Constant
# Object that represents a constant
# --------------------------------------------------

class Constant:
    def __init__(self, address, name, type, value):
        self.address = address
        self.name = name
        self.type = type
        self.value = value
    
    def __str__(self) -> str:
        return 'Constant: ' + str(self.name) + ', ' + str(self.type) + ', ' + str(self.address)
