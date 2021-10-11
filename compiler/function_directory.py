# ------------ function_directory.py ------------
# -- Rodrigo Bilbao -- Isabella Canales --
# 
# -- Lumos : Function Directory
# -----------------------------------------------

class Function:
    def __init__(self, name, type, parameters, varTable):
        self.name = name
        self.type = type
        self.parameters = parameters
        self.varTable = varTable

class FunctionDirectory:
    def __init__(self):
        self.functions = {}

    def find(self, function):
        if function.name in self.function:
            return self.variables[function.name]
        else:
            return None

    def insert(self, function):
        if self.find(function) is not None:
            print("Invalid function: '", function.name, " is already declared.")
        else:
            self.variables[function.name] = function
            return self.variables[function.name]
        return 0;
    
    def clear(self):
        self.function.clear()
        