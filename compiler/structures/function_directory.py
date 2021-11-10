# ------------ function_directory.py ------------
# -- Rodrigo Bilbao -- Isabella Canales --
# 
# -- Lumos : Function Directory
# -----------------------------------------------

class Function:
    def __init__(self, name, type, parameters, quadruplePosition, memoryLimits):
        self.name = name
        self.type = type
        self.parameters = parameters
        self.quadruplePosition = quadruplePosition
        self.limits = memoryLimits

class FunctionDirectory:
    def __init__(self):
        self.functions = {}

    def find(self, function):
        if function.name in self.functions:
            return self.functions[function.name]
        else:
            return None

    def insert(self, function):
        if self.find(function) is not None:
            print("Invalid function: '", function.name, " is already declared.")
        else:
            self.functions[function.name] = function
            return self.functions[function.name]
        return 0;
    
    def clear(self):
        self.functions.clear()
        