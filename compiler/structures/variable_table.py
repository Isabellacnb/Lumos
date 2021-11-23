# -------------- variable_table.py --------------
# -- Rodrigo Bilbao -- Isabella Canales --
# 
# -- Lumos : Variable Table
# -----------------------------------------------

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


        

        

