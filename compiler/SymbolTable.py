class SymbolTable():
    def __init__(self, symbols):
        self.symbols = symbols
    
    def getter(self, key):
        if key in self.symbols:
            return self.symbols[key]
        raise Exception("KeyError")
    
    def setter(self, key, value):
        if key not in self.symbols:
            raise Exception("Variable not declared")
        if self.symbols[key][1] != value[1]:
            raise Exception("TypeError")
        self.symbols[key] = value

    def create_variable(self, name, value, type):
        if name in self.symbols:
            raise Exception("Variable already declared")
        if value == None:
            if type ==  "i32":
                self.symbols[name] = (0, type)
            elif type == "bool":
                self.symbols[name] = (False, type)
            elif type == "str":
                self.symbols[name] = ("", type)
        else:
            if value[1] != type:
                raise Exception("TypeError: declared type does not match assigned value")
            self.symbols[name] = value
