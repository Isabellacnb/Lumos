from structures import *

class ActivationRecord:
    def __init__(self, memoryLimits):
        self.parameters = []
        self.localAddresses = memoryLimits[0]
        self.temporaryAddresses = memoryLimits[1]
        #TODO: parameters, call position, return address

        self.size = 20000

        self.localMemory = {}
        for type in Type:
            if type == Type.VOID:
                continue
            self.localAddresses[type] = (self.localAddresses[type] % self.size) * [None]
        
        self.temporaryMemory = {}
        for type in Type:
            if type == Type.VOID:
                continue
            self.temporaryMemory[type] = (self.temporaryMemory[type] % self.size) * [None]

    def set(self, scope, address, value, addressType):
        if (scope == Scope.TEMPORARY):
            for type in Type:
                if addressType == type:
                    self.temporaryMemory[type.value][address] = value
                    return
        elif (scope == Scope.LOCAL):
            for type in Type:
                if addressType == type:
                    self.localMemory[type.value][address] = value
                    return

    def get(self, scope, address, addressType):
        if (scope == Scope.TEMPORARY):
            for type in Type:
                if addressType == type:
                    return self.temporaryMemory[type.value][address]
        elif (scope == Scope.LOCAL):
            for type in Type:
                if addressType == type:
                    return self.localMemory[type.value][address]
    