class SymbolTable():
    def __init__(self, symbols, parent=None):
        self.symbols = symbols
        self.parent = parent
    
    """ V2.3
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
    """
    def getter(self, key):
        current = self
        while current is not None:
            if key in current.symbols:
                return current.symbols[key]
            current = current.parent
        raise Exception(f"KeyError: '{key}' not found in any scope")

    def setter(self, key, value):
        current = self
        while current is not None:
            if key in current.symbols:
                if current.symbols[key][1] != value[1]:
                    raise Exception("TypeError: incompatible types")
                current.symbols[key] = value
                return
            current = current.parent
        raise Exception(f"Variable '{key}' not declared in any accessible scope")

    def create_variable(self, name, value, type, func_or_var):
        if name in self.symbols:
            raise Exception("Variable already declared")
        if value == None:
            if type ==  "i32":
                self.symbols[name] = (0, type, func_or_var)
            elif type == "bool":
                self.symbols[name] = (False, type, func_or_var)
            elif type == "str":
                self.symbols[name] = ("", type, func_or_var)
        else:
            if value[1] != type:
                raise Exception("TypeError: declared type does not match assigned value")
            self.symbols[name] = value
