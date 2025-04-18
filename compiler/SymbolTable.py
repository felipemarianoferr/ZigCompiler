class SymbolTable():
    def __init__(self, symbols):
        self.symbols = symbols
        self.offset = 0
    
    def getter(self, key):
        if key in self.symbols:
            return self.symbols[key][:2]
        raise Exception("KeyError")
    
    def setter(self, key, value):
        if key not in self.symbols:
            raise Exception("Variable not declared")
        if self.symbols[key][1] != value[1]:
            raise Exception("TypeError")
        self.symbols[key] = (value[0], value[1], self.symbols[key][2])

    def getter_offset(self, key):
        if key not in self.symbols:
            raise Exception("Variable not declared")
        offset = self.symbols[key][2]
        if offset < 0:
            return f"{offset}"
        else:
            return f"+{offset}"

    def create_variable(self, name, value, var_type):
        if name in self.symbols:
            raise Exception("Variable already declared")
        
        self.offset -= 4
        
        if value is None:
            if var_type == "i32":
                default = 0
            elif var_type == "bool":
                default = False
            elif var_type == "str":
                default = ""
            else:
                raise Exception("Unknown type")
            self.symbols[name] = (default, var_type, self.offset)
        else:
            if value[1] != var_type:
                raise Exception("TypeError: declared type does not match assigned value")
            self.symbols[name] = (value[0], var_type, self.offset)
