# -------------- variable_table.py --------------
# -- Rodrigo Bilbao -- Isabella Canales --
# 
# -- Lumos : Variable Table
# Object that represents a variable table, which
# is used to store the variables generated 
# throughout our compiler allowing methods of search 
# and inserting. It verifies whether a variable is 
# already declared before inserting it, as well as 
# finding and returing a specific variable based on 
# the given name.
# --------------------------------------------------

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


        

        

