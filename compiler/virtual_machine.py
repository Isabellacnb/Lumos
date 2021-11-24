import sys
import logging
from datetime import datetime
from enum import Enum
from os.path import exists
from memory.activation_record import ActivationRecord
from memory.memory_manager import MemoryManager

from structures import *

class Phase(Enum):
    MEMORY = 0
    FUNCDIR = 1
    CONSTANTS = 2
    QUADS = 3

class VirtualMachine:
    def __init__(self, file_path):
        self.file_path = file_path
        self.quad_list = QuadrupleList()
        self.funcDir = FunctionDirectory()
        self.constantTable = VariableTable()

        self.globalAddresses = {}
        self.localAddresses = {}
        self.tempAddresses = {}
        self.cteAddresses = {}

        self.load_file()

        self.memoryManager = MemoryManager(self.globalAddresses, self.localAddresses, self.tempAddresses, self.cteAddresses)
        self.currFuncCall = None
        for const in self.constantTable.variables.values():
            self.memoryManager.set(const.address, const.value)
    
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
                if "@MEMORY" in line:
                    phase = Phase.MEMORY
                    continue
                elif "@FUNCTIONS" in line:
                    phase = Phase.FUNCDIR
                    continue
                elif "@CONSTANTS" in line:
                    phase = Phase.CONSTANTS
                    continue
                elif "@QUADS" in line:
                    phase = Phase.QUADS
                    continue

                # Based on phase, perform loading
                if phase == Phase.MEMORY:
                    # scope | bool | int | float | char | string
                    memoryElements = line.split('|')
                    memoryScope = memoryElements[0]
                    memoryDict = {}
                    for t in Type:
                        if t == Type.VOID:
                            continue
                        memoryDict[t] = int(memoryElements[t.value + 1])
                    self.assignDict(memoryScope, memoryDict)

                elif phase == Phase.FUNCDIR:
                    # name|returnType|{paramName!paramType!paramAddress#}|quadPosition|localLimitsArray|tempLimitsArray
                    funcElements = line.split('|')
                    funcName = funcElements[0]
                    funcType = Type(int(funcElements[1]))
                    
                    funcParams = []
                    params = funcElements[2].split('#')
                    for param in params:
                        paramElements = param.split("!")
                        paramVar = Variable(paramElements[0], Type(int(paramElements[1])))
                        paramVar.address = int(paramElements[2])
                        funcParams.append(paramVar)
                    
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
                    quad = Quadruple(quadElements[1], quadElements[2], quadElements[3], quadElements[4][:-1])
                    self.quad_list.push(quad)
        # except Exception as e:
        #     print("ERROR :: DURING OBJECT CODE LOADING AN ERROR OCCURED", e)
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
        elif "True" in value:
            return True
        elif "False" in value:
            return False
        else:
            return int(value)
    
    def assignDict(self, memoryScope, memoryDict):
        if memoryScope == "global":
            self.globalAddresses = memoryDict
        elif memoryScope == "local":
            self.localAddresses = memoryDict
        elif memoryScope == "temp":
            self.tempAddresses = memoryDict
        elif memoryScope == "constant":
            self.cteAddresses = memoryDict

    # ============================
    # Executioner
    # ============================
    def run(self):
        inst_ptr = 0

        # Switch case to execute quadruple by quadruple 
        while (True):
            quad = self.quad_list.at(inst_ptr)
            operation = quad.operator

            if operation == "GOTO":
                logging.debug("GOTO exectued")
                inst_ptr = int(quad.result)
                continue

            elif operation == "GOTOF":
                logging.debug("GOTOF executed")
                condition = self.memoryManager.get(quad.operLeft)
                if condition == False:
                    inst_ptr = int(quad.result)
                    continue
            
            elif operation == "GOSUB":
                logging.debug("GOSUB executed")
                func = self.funcDir.find(quad.operLeft)
                #TODO check if necessary
                # if len(func.parameters) != len(self.memoryManager.callStack.top().parameters):
                #     print("ERROR :: Incorrect number of arguments given when calling", func.name, ", expected", len(func.paramters), "got", len(self.memoryManager.callStack.top().parameters))
                #     exit()
                
                if quad.result != "None":
                    self.memoryManager.callStack.top().returnAddress = int(quad.result)
                
                self.memoryManager.callStack.top().callbackPosition = inst_ptr + 1

                inst_ptr = func.quadruplePosition
                continue

            elif operation == "ERA":
                logging.debug("ERA executed")
                func = self.funcDir.find(quad.operLeft)
                act_record = ActivationRecord(func.limits)
                self.memoryManager.callStack.push(act_record)
                self.currFuncCall = func.name
            
            elif operation == "PARAM":
                logging.debug("PARAM executed")
                func = self.funcDir.find(self.currFuncCall)
                paramInd = int(quad.result)

                act_record = self.memoryManager.callStack.pop()
                paramValue = self.memoryManager.get(quad.operLeft)
                paramScope = self.memoryManager.getScopeOf(int(quad.operLeft))
                paramType = self.memoryManager.getTypeOf(int(quad.operLeft), paramScope)
                self.memoryManager.callStack.push(act_record)

                if func.parameters[paramInd].type != paramType:
                    print("ERROR :: Type mismatch when calling", func.name, "expected", func.parameters[paramInd].type, "got", paramType.name)
                    exit()

                self.memoryManager.set(func.parameters[paramInd].address, paramValue)

            elif operation == "ENDFUNC":
                logging.debug("ENDFUNC executed")

                inst_ptr = self.memoryManager.callStack.top().callbackPosition
                continue

            elif operation == "RETURN":
                logging.debug("RETURN executed")
                returnAddress = self.memoryManager.callStack.top().returnAddress
                value = self.memoryManager.get(quad.result)
                self.memoryManager.set(returnAddress, value)
                
                inst_ptr = self.memoryManager.callStack.top().callbackPosition

                self.memoryManager.callStack.pop()
                continue

            elif operation == "PRINT":
                logging.debug("PRINT executed")
                value = self.memoryManager.get(quad.result)
                print(value, end="")

            elif operation == "PRINTLN":
                logging.debug("PRINTLN executed")
                print('\n', end="")

            elif operation == "READ":
                logging.debug("READ executed")
                readValue = input()
                self.memoryManager.set(quad.result, readValue)

            elif operation == "=":
                logging.debug("ASSIGN executed")

                value = self.memoryManager.get(quad.operLeft)
                self.memoryManager.set(quad.result, value)

            # Arithmetic operations
            elif operation in ["+", "-", "*", "/", ">", "<", ">=", "<=", "<>", "=="]:
                self.arithmeticOperations(quad)
            
            elif operation == "END":
                logging.debug("END executed")
                print("Mischief managed")
                return
            
            inst_ptr += 1
            
    def arithmeticOperations(self, quad):
        operation = quad.operator
        left = self.memoryManager.get(quad.operLeft)
        right = self.memoryManager.get(quad.operRight)
        
        if operation == "+":
            logging.debug("SUM executed")
            self.memoryManager.set(quad.result, left + right)
        elif operation == "-":
            logging.debug("SUB executed")
            self.memoryManager.set(quad.result, left - right)
        elif operation == "*":
            logging.debug("MULT executed")
            self.memoryManager.set(quad.result, left * right)
        elif operation == "/":
            logging.debug("DIV executed")
            if right == 0:
                print("ERROR :: Division by zero")
                exit()
            self.memoryManager.set(quad.result, left / right)
        elif operation == ">":
            logging.debug("MORETHAN executed")
            self.memoryManager.set(quad.result, left > right)
        elif operation == "<":
            logging.debug("LESSTHAN executed")
            self.memoryManager.set(quad.result, left < right)
        elif operation == ">=":
            logging.debug("MORETHANEQL executed")
            self.memoryManager.set(quad.result, left >= right)
        elif operation == "<=":
            logging.debug("LESSTHANEQL executed")
            self.memoryManager.set(quad.result, left <= right)
        elif operation == "<>":
            logging.debug("NOT executed")
            self.memoryManager.set(quad.result, left != right)
        elif operation == "==":
            logging.debug("EQUAL executed")
            self.memoryManager.set(quad.result, left == right)



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
    exe_time = end_time - start_time
    logging.debug("EXECUTION COMPLETED in " + str(exe_time.total_seconds()) + " secs")