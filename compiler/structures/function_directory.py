# ------------ function_directory.py ------------
# -- Rodrigo Bilbao -- Isabella Canales --
# 
# -- Lumos : Function Directory
# Object that represents a function directory, which
# is used to store the functions contained in a
# program. It verifies whether a function is already
# declared before inserting it, as well as finding
# and returing a specific function based on the name
# given.
# --------------------------------------------------

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
            print("ERROR :: Invalid function: '", function.name, " is already declared.")
            exit()
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
        