from structures import *

class ActivationRecord:
    def __init__(self, memoryLimits):
        self.parameters = []
        self.localAddresses = memoryLimits[0]
        self.temporaryAddresses = memoryLimits[1]
        #TODO: parameters, call position, return address

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
    