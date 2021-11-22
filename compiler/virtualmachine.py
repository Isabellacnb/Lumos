import sys
import logging
from datetime import datetime
from enum import Enum
from os.path import exists

from structures import *

class Phase(Enum):
    FUNCDIR = 0
    CONSTANTS = 1
    QUADS = 2

class VirtualMachine:
    def __init__(self, file_path):
        self.file_path = file_path
        self.quad_list = QuadrupleList()
        self.funcDir = FunctionDirectory()
        self.constantTable = VariableTable()

        self.load_file()
    
    def load_file(self):
        if not exists(self.file_path):
            print("ERROR :: File ", self.file_path, "not found")
            exit()

        reader = open(self.file_path)

        try:
            # Process object code file
            lines = reader.readlines()
            logging.debug(lines)

            phase = Phase.FUNCDIR

            for line in lines:
                # Check if we have reached new loading phase
                if "@FUNCTIONS" in line:
                    phase = Phase.FUNCDIR
                    continue
                elif "@CONSTANTS" in line:
                    phase = Phase.CONSTANTS
                    continue
                elif "@QUADS" in line:
                    phase = Phase.QUADS
                    continue

                # Based on phase, perform loading
                if phase == Phase.FUNCDIR:
                    # name|returnType|paramTypeArray|quadPosition|localLimitsArray|tempLimitsArray
                    funcElements = line.split('|')
                    funcName = funcElements[0]
                    funcType = Type(int(funcElements[1]))
                    params = funcElements[2][1:-1].split(',')
                    funcParams = list(map(lambda x: Type(int(x)), params))
                    funcPos = int(funcElements[3])
                    
                    localLimits = funcElements[4][1:-1].split(',')
                    funcLocalLimits = list(map(lambda x: int(x), localLimits))
                    localLimits = self.limitsToDict(funcLocalLimits)
                    
                    tempLimits = funcElements[5][1:-2].split(',')
                    funcTempLimits = list(map(lambda x: int(x), tempLimits))
                    tempLimits = self.limitsToDict(funcTempLimits)

                    func = Function(funcName, funcType, funcParams, funcPos, (localLimits, tempLimits))
                    self.funcDir.insert(func)

                if phase == Phase.CONSTANTS:
                    # name|type|value|address
                    constElements = line.split('|')
                    constName = constElements[0]
                    constType = Type(int(constElements[1]))
                    constValue = self.valueToConstant(constElements[2])
                    
                    constAddress = int(constElements[3])

                    constant = Constant(constAddress, constName, constType, constValue)
                    self.constantTable.insert(constant)

                if phase == Phase.QUADS:
                    # operation | 2nd ele | 3rd ele | result
                    quadElements = line.split('|')
                    quad = Quadruple(quadElements[0], quadElements[1], quadElements[2], quadElements[3])
                    self.quad_list.push(quad)
        except Exception as e:
            print("ERROR :: DURING OBJECT CODE LOADING AN ERROR OCCURED", e)
        finally:
            reader.close()

        logging.debug("LOAD_FILE :: Successfully loaded", self.file_path)
        
    # ============================
    # Helper functions to load object code
    # ============================
    def limitsToDict(self, limits_array):
        limits_dict = {}
        for type in Type:
            if type == Type.VOID:
                continue
            limits_dict[type] = limits_array[type.value]
        
        return limits_dict
    
    def valueToConstant(self, value):
        if "\"" in value and len(value) > 1:
            return value[1:-1]
        elif "\"" in value:
            return value[1:-1]
        elif "." in value:
            return float(value)
        elif "true" in value:
            return True
        elif "false" in value:
            return False
        else:
            return int(value)

    # ============================
    # Executioner
    # ============================
    def run(self):
        inst_ptr = 0

        # Switch case to execute quadruple by quadruple 
        for quad in self.quad_list:
            operation = quad[0]

            if operation == "GOTO":
                logging.debug("GOTO exectued")

            elif operation == "GOTOF":
                logging.debug("GOTOF executed")

            elif operation == "END":
                logging.debug("END executed")

            elif operation == "ENDFUNC":
                logging.debug("ENDFUNC executed")

            elif operation == "RETURN":
                logging.debug("RETURN executed")

            elif operation == "PRINT":
                logging.debug("PRINT executed")

            elif operation == "PRINTLN":
                logging.debug("PRINTLN executed")

            elif operation == "READ":
                logging.debug("READ executed")
            
            elif operation == "=":
                logging.debug("ASSIGN executed")

            # Arithmetic operations
            elif operation == "+":
                logging.debug("SUM executed")
            elif operation == "-":
                logging.debug("SUB executed")
            elif operation == "*":
                logging.debug("MULT executed")
            elif operation == "/":
                logging.debug("DIV executed")
            elif operation == ">":
                logging.debug("MORETHAN executed")
            elif operation == "<":
                logging.debug("LESSTHAN executed")
            elif operation == ">=":
                logging.debug("MORETHANEQL executed")
            elif operation == "<=":
                logging.debug("LESSTHANEQL executed")
            elif operation == "<>":
                logging.debug("NOT executed")
            elif operation == "==":
                logging.debug("EQUAL executed")
            


if __name__ == "__main__":
    # DEBUG mechanism
    if "-debug" in sys.argv:
        logging.basicConfig(level=logging.DEBUG)
    
    if len(sys.argv) < 2:
        print("ERROR :: Not file name specified")
        exit()

    file_path = sys.argv[1]
    virtual_machine = VirtualMachine(file_path)
    
    start_time = datetime.now()
    virtual_machine.run()
    end_time = datetime.now()

    logging.debug("EXECUTION COMPLETED in", end_time - start_time)