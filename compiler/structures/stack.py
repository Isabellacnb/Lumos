class Stack:
    def __init__(self):
        self.items = []
    
    def pop(self):
        return self.items.pop()

    def push(self, item):
        self.items.append(item)

    def empty(self):
        return len(self.items) == 0

    def clear(self):
        self.items.clear()

    def top(self):
        if len(self.items) == 0:
            print("STACK EMPTY")
        else:
            return self.items[-1]

    def size(self):
        return len(self.items)

    def __str__(self) -> str:
        string = "[ "

        for item in self.items:
            string += str(item) + " "

        string += "]"
        return string