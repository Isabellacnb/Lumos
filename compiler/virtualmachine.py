import sys
import logging
from datetime import datetime
from enum import Enum
from os.path import exists

class Phase(Enum):
    FUNCDIR = 0
    CONSTANTS = 1
    QUADS = 2

class VirtualMachine:
    def __init__(self, file_path):
        self.file_path = file_path
        self.quad_list = None
        self.funcDir = None

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
                if line == "@CONSTANTS":
                    phase = Phase.CONSTANTS
                elif line == "@QUADS":
                    phase = Phase.QUADS

                # Based on phase, perform loading
                if phase == Phase.FUNCDIR:
                    pass
                if phase == Phase.CONSTANTS:
                    pass
                if phase == Phase.QUADS:
                    pass

        except Exception as e:
            print(e)
        finally:
            reader.close()
        
        logging.debug("LOAD_FILE :: Successfully loaded", self.file_path)
        
    
    def run(self):
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