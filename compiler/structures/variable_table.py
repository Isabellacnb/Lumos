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

class VariableTable:
    def __init__(self):
        self.variables = {}

    def find(self, variable):
        if variable.name in self.variables:
            return self.variables[variable.name]
        else:
            return None

    def insert(self, variable):
        if self.find(variable) is not None:
            print("Invalid variable: '", variable.name, " is already declared.")
        else:
            self.variables[variable.name] = variable
            return self.variables[variable.name]
        return 0;
    
    def clear(self):
        self.variables.clear()
        

        

