# -------------- variable_table.py --------------
# -- Rodrigo Bilbao -- Isabella Canales --
# 
# -- Lumos : Constant
# -----------------------------------------------

class Constant:
    def __init__(self, address, name, type, value):
        self.address = address
        self.name = name
        self.type = type
        self.value = value
    
    def address(self):
        return self.address
    
    def __str__(self) -> str:
        return 'Constant: ' + str(self.name) + ', ' + str(self.type) + ', ' + str(self.address)
