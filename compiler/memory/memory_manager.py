from structures import *

class MemoryManager:
    def __init__(self, memoryLimits):
        self.globalAddresses = memoryLimits[0]
        self.localAddresses = memoryLimits[1]
        self.tempAddresses = memoryLimits[2]
        self.cteAddresses = memoryLimits[3]

        self.size = 20000

        self.globalMemory = {}
        for idx, t in enumerate(Type):
            if t == Type.Void:
                continue
            self.globalMemory[t] = (self.globalAddresses[t] % self.size) * [None]



