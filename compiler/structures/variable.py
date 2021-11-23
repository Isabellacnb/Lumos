# -------------- variable_table.py --------------
# -- Rodrigo Bilbao -- Isabella Canales --
# 
# -- Lumos : Variable
# -----------------------------------------------

class Variable:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.address = -1
        self.value = None
    
    def __str__(self) -> str:
        return "[" + self.name + " " + str(self.type) + " " + str(self.address) + "]"