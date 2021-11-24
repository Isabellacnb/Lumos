from structures import *
from .activation_record import ActivationRecord

class MemoryManager:
    def __init__(self, g, l, t, c):
        self.globalAddresses = g
        self.localAddresses = l
        self.tempAddresses = t
        self.cteAddresses = c
        
        self.size = 20000

        # Activation Record
        self.executeStack = Stack()
        self.apparateStack = Stack()
        self.executeStack.push(ActivationRecord((self.localAddresses, self.tempAddresses)))

        # Create arrays with the n number of addresses used
        self.baseSize = self.size // (len(Type) - 1)
        self.globalMemory = {}
        for type in Type:
            if type == Type.VOID:
                continue
            self.globalMemory[type] = (self.globalAddresses[type] % self.baseSize) * [None]
        
        self.cteMemory = {}
        for type in Type:
            if type == Type.VOID:
                continue
            self.cteMemory[type] = (self.cteAddresses[type] % self.baseSize) * [None]
    
    def get(self, address):
        address = int(address) # safe check

        addressScope = self.getScopeOf(address)
        addressType = self.getTypeOf(address, addressScope)
        address = address % self.baseSize

        if addressScope == Scope.GLOBAL:
            return self.globalMemory[addressType][address]
        elif addressScope == Scope.CONSTANT:
            return self.cteMemory[addressType][address]
        # Handled by Activation Record as it's temp or local
        else:
            return self.executeStack.top().get(addressScope, address, addressType)

    def set(self, address, value):
        address = int(address) # safe check

        addressScope = self.getScopeOf(address)
        addressType = self.getTypeOf(address, addressScope)
        address = address % self.baseSize

        if addressScope == Scope.GLOBAL:
            value = self.stringToType(value, addressType)
            self.globalMemory[addressType][address] = value
        elif addressScope == Scope.CONSTANT:
            value = self.stringToType(value, addressType)
            self.cteMemory[addressType][address] = value
        else:
            value = self.stringToType(value, addressType)
            self.executeStack.top().set(addressScope, address, value, addressType)

    # ==================
    # Inner management functions
    # ================== 
    
    # Get the scope of an address based on the range   
    def getScopeOf(self, address):
        if self.size * 0 <= address < self.size * 1:
            return Scope.GLOBAL
        elif self.size * 1 <= address < self.size * 2:
            return Scope.LOCAL
        elif self.size * 2 <= address < self.size * 3:
            return Scope.TEMPORARY
        elif self.size * 3 <= address < self.size * 4:
            return Scope.CONSTANT
    
    # Get the Type based on the address and scope given
    def getTypeOf(self, address, scope):
        if scope == Scope.LOCAL:
            address = address % self.size
        elif scope == Scope.TEMPORARY:
            address = address % (self.size * 2)
        elif scope == Scope.CONSTANT:
            address = address % (self.size * 3)

        baseOfTypes = (self.size / (len(Type) - 1))
        for idx, type in enumerate(Type):
            if type == Type.VOID:
                continue
            elif baseOfTypes * idx <= address < baseOfTypes * (idx + 1):
                return type  
    
    # Translate string to the specified type
    def stringToType(self, value, type):
        if not isinstance(value, str):
            return value
        elif type == Type.BOOL:
            return True if value == "true" or value == "True" else False
        elif type == Type.INT:
            return int(value)
        elif type == Type.FLOAT:
            return float(value)
        elif type == Type.CHAR or type == Type.STRING:
            return value      


