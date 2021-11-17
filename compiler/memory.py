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
            #print("GLOBAL", type, "START", self.globalAddresses[type])
            #print("LOCAL", type, "START", self.localAddresses[type])
            #print("TEMP", type, "START", self.tempAddresses[type])
            #print("CTE", type, "START", self.cteAddresses[type])

    def nextAddress(self, scope, type, size=1):
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
    
    def resetAddresses(self):
        for idx, type in enumerate(Type):
            if type == Type.VOID:
                break
            self.localAddresses[type] = self.space * 1 + idx * self.typeRange
            self.tempAddresses[type] = self.space * 2 + idx * self.typeRange
    
    def getLimits(self):
        for idx, type in enumerate(Type):
            if type == Type.VOID:
                break
            local = self.space * 1 + idx * self.typeRange
            temp = self.space * 2 + idx * self.typeRange
            local = self.localAddresses[type] - local
            temp = self.tempAddresses[type] - temp

        return (local, temp)
        

# ad = AddressManager()
# print(ad.nextAddress(Scope.GLOBAL, Type.INT))
# print(ad.nextAddress(Scope.GLOBAL, Type.INT))
# print(ad.nextAddress(Scope.LOCAL, Type.INT))
# print(ad.nextAddress(Scope.LOCAL, Type.INT))

# ad.resetAddresses()
# print(ad.nextAddress(Scope.LOCAL, Type.INT))
# print(ad.nextAddress(Scope.LOCAL, Type.INT))