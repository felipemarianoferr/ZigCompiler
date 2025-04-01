class SymbolTable():
    def __init__(self, symbols):
        self.symbols = symbols
    
    def getter(self, key):
        if key in self.symbols:
            return self.symbols[key]
        raise Exception("KeyError")
    
    def setter(self, key, value):
        self.symbols[key] = value