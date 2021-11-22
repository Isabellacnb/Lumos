# Structures
from structures import *

class AddressManager:

    def __init__(self):
        self.globalAddresses = {}
        self.localAddresses = {}
        self.tempAddresses = {}
        self.cteAddresses = {}

        self.space = 20000
        self.typeRange = self.space // (len(Type) - 1)

        for idx, type in enumerate(Type):
            if type == Type.VOID:
                break
            self.globalAddresses[type] = self.space * 0 + idx * self.typeRange
            self.localAddresses[type] = self.space * 1 + idx * self.typeRange
            self.tempAddresses[type] = self.space * 2 + idx * self.typeRange
            self.cteAddresses[type] = self.space * 3 + idx * self.typeRange
            print("GLOBAL", type, "START", self.globalAddresses[type])
            print("LOCAL", type, "START", self.localAddresses[type])
            print("TEMP", type, "START", self.tempAddresses[type])
            print("CTE", type, "START", self.cteAddresses[type])

    def nextAddress(self, scope, type, size=1):
        #TODO: Check next address is not out of bounds
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
            raise("ERROR: When trying to generate a new address the following problem was found:", e)
    
    def resetAddresses(self):
        for idx, type in enumerate(Type):
            if type == Type.VOID:
                break
            self.localAddresses[type] = self.space * 1 + idx * self.typeRange
            self.tempAddresses[type] = self.space * 2 + idx * self.typeRange
    
    def getLimits(self):
        local = self.localAddresses
        temp = self.tempAddresses
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