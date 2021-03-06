# -------------- address_manager.py --------------
# -- Rodrigo Bilbao -- Isabella Canales --
# 
# -- Lumos : Address Manager
# Object that represents an address manager. An 
# address manager is used during the compilation 
# phase for generating addresses based on type, 
# scope and size of variables, as well as providing 
# memory limits for each scope addresses.
# --------------------------------------------------

from structures import *

class AddressManager:

    def __init__(self):
        self.globalAddresses = {}
        self.localAddresses = {}
        self.tempAddresses = {}
        self.cteAddresses = {}

        self.size = 20000
        self.typeRange = self.size // (len(Type) - 1)

        for idx, type in enumerate(Type):
            if type == Type.VOID:
                break
            self.globalAddresses[type] = self.size * 0 + idx * self.typeRange
            self.localAddresses[type] = self.size * 1 + idx * self.typeRange
            self.tempAddresses[type] = self.size * 2 + idx * self.typeRange
            self.cteAddresses[type] = self.size * 3 + idx * self.typeRange

    def nextAddress(self, scope, type, size=1):
        try:
            if (scope == Scope.GLOBAL):
                address = self.globalAddresses[type]
                self.globalAddresses[type] += size
            elif (scope == Scope.LOCAL):
                address = self.localAddresses[type]
                self.localAddresses[type] += size
            elif (scope == Scope.TEMPORARY):
                address = self.tempAddresses[type]
                self.tempAddresses[type] += size
            elif (scope == Scope.CONSTANT):
                address = self.cteAddresses[type]
                self.cteAddresses[type] += size
            
            return address
        except Exception as e:
            raise("ERROR :: When trying to generate a new address the following problem was found:", e)
    
    def resetAddresses(self):
        for idx, type in enumerate(Type):
            if type == Type.VOID:
                break
            self.localAddresses[type] = self.size * 1 + idx * self.typeRange
            self.tempAddresses[type] = self.size * 2 + idx * self.typeRange
    
    def getLimits(self):
        local = self.localAddresses.copy()
        temp = self.tempAddresses.copy()
        return (local, temp)
        


'''
ADDRESS SYSTEM MAP:
<GLOBAL>: 
    bool: 0
     int: 4000
   float: 8000
    char: 12000
  string: 16000

<LOCAL>:
    bool: 20000
     int: 24000
   float: 28000
    char: 32000
  string: 36000

<TEMPORARY>:
    bool: 40000
     int: 44000
   float: 48000
    char: 52000
  string: 56000

<CONSTANT>:
    bool: 60000
     int: 64000
   float: 68000
    char: 72000
  string: 76000

'''