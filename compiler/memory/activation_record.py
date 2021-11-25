# -------------- activation_record.py --------------
# -- Rodrigo Bilbao -- Isabella Canales --
# 
# -- Lumos : Activation Record
# Object that represents an activation record. An 
# activation record is used during execution phase 
# for the control and management of the local and 
# temporary memory as well as callback functionality 
# during task invoking. 
# --------------------------------------------------

from structures import *

class ActivationRecord:
    def __init__(self, memoryLimits):
        self.parameters = []
        self.localAddresses = memoryLimits[0]
        self.temporaryAddresses = memoryLimits[1]
        self.callbackPosition = -1
        self.returnAddress = -1

        self.size = 20000

        self.baseSize = self.size // (len(Type) - 1)
        self.localMemory = {}
        for type in Type:
            if type == Type.VOID:
                continue
            self.localMemory[type] = (self.localAddresses[type] % self.baseSize) * [None]
        
        self.temporaryMemory = {}
        for type in Type:
            if type == Type.VOID:
                continue
            self.temporaryMemory[type] = (self.temporaryAddresses[type] % self.baseSize) * [None]

    def set(self, scope, address, value, addressType):
        if (scope == Scope.TEMPORARY):
            for type in Type:
                if addressType == type:
                    self.temporaryMemory[type][address] = value
                    return
        elif (scope == Scope.LOCAL):
            for type in Type:
                if addressType == type:
                    self.localMemory[type][address] = value
                    return

    def get(self, scope, address, addressType):
        if (scope == Scope.TEMPORARY):
            for type in Type:
                if addressType == type:
                    return self.temporaryMemory[type][address]
        elif (scope == Scope.LOCAL):
            for type in Type:
                if addressType == type:
                    return self.localMemory[type][address]
    