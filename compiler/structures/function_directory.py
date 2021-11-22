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
    
    def __str__(self):
        return "Function: " + str(self.name) + " (" + str(self.type) + ") - " + str(self.parameters) + " - " + str(self.quadruplePosition) + "(quad position)" + str(self.limits)

class FunctionDirectory:
    def __init__(self):
        self.functions = {}

    def find(self, function):
        if function in self.functions:
            return self.functions[function]
        else:
            return None

    def insert(self, function):
        if self.find(function) is not None:
            print("Invalid function: '", function.name, " is already declared.")
        else:
            self.functions[function.name] = function
            return self.functions[function.name]
        return 0
    
    def clear(self):
        self.functions.clear()

    def __str__(self):
        output = ""
        
        for function in self.functions.values():
            output += str(function) + "\n"

        return output
        