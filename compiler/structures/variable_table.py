# -------------- variable_table.py --------------
# -- Rodrigo Bilbao -- Isabella Canales --
# 
# -- Lumos : Variable Table
# -----------------------------------------------

class Variable:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.address = -1
        self.value = None
    
    def __str__(self) -> str:
        return "[" + self.name + " " + str(self.type) + " " + str(self.address) + "]"

class Constant:
    def __init__(self, address, name, type, value):
        self.address = address
        self.name = name
        self.type = type
        self.value = value
    
    def address(self):
        return self.address
    
    def __str__(self) -> str:
        return 'Constant: ' + self.name + ', ' + self.type + ', ' + str(self.address())

class VariableTable:
    def __init__(self):
        self.variables = {}

    def find(self, name):
        if name in self.variables:
            return self.variables[name]
        else:
            return None

    def insert(self, variable):
        if self.find(variable) is not None:
            print("Invalid variable: '", variable.name, " is already declared.")
        else:
            self.variables[variable.name] = variable
            return self.variables[variable.name]
        return 0
    
    def clear(self):
        self.variables.clear()
    
    def __str__(self) -> str:
        string = "{\n"
        for var in self.variables.values():
            string += str(var) + "\n"
        
        return string + "}"


        

        

