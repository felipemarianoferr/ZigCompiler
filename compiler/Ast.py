from compiler.SymbolTable import SymbolTable
import sys

class Node():
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def Evaluate(self, st):
        pass

class BinOp(Node):
    def Evaluate(self, st):
        tuple1 = self.children[0].Evaluate(st)
        tuple2 = self.children[1].Evaluate(st)
        if self.value == '+':
            if tuple1[1] == 'i32' and tuple2[1] == 'i32':
                return (tuple1[0] + tuple2[0], 'i32')
            else:
                raise TypeError("TypeError: operator '+' only supports i32")
        elif self.value == '-':
            if tuple1[1] == 'i32' and tuple2[1] == 'i32':
                return (tuple1[0] - tuple2[0], 'i32')
            else:
                raise TypeError("TypeError: operator '-' only supports i32")
        elif self.value == '*':
            if tuple1[1] == 'i32' and tuple2[1] == 'i32':
                return (tuple1[0] * tuple2[0], 'i32')
            else:
                raise TypeError("TypeError: operator '*' only supports i32")
        elif self.value == '/':
            if tuple1[1] == 'i32' and tuple2[1] == 'i32':
                if tuple2[0] == 0:
                    raise ZeroDivisionError("Division by zero")
                return (tuple1[0] // tuple2[0], 'i32')
            else:
                raise TypeError("TypeError: operator '/' only supports i32")
        elif self.value == '||':
             if tuple1[1] == 'bool' and tuple2[1] == 'bool':
                 val1 = True if tuple1[0] == 'true' else False
                 val2 = True if tuple2[0] == 'true' else False
                 return ('true' if val1 or val2 else 'false', 'bool')
             else:
                 raise TypeError("TypeError: operator '||' only supports bool")
        elif self.value == '&&':
             if tuple1[1] == 'bool' and tuple2[1] == 'bool':
                 val1 = True if tuple1[0] == 'true' else False
                 val2 = True if tuple2[0] == 'true' else False
                 return ('true' if val1 and val2 else 'false', 'bool')
             else:
                 raise TypeError("TypeError: operator '&&' only supports bool")
        elif self.value == '==':
             if tuple1[1] == tuple2[1] and tuple1[1] in ['i32', 'bool', 'str']:
                 return ('true' if tuple1[0] == tuple2[0] else 'false', 'bool')
             else:
                 raise TypeError(f"TypeError: operator '==' cannot compare types '{tuple1[1]}' and '{tuple2[1]}'")
        elif self.value == '<':
            if tuple1[1] == 'i32' and tuple2[1] == 'i32':
                 return ('true' if tuple1[0] < tuple2[0] else 'false', 'bool')
            elif tuple1[1] == 'str' and tuple2[1] == 'str':
                 return ('true' if tuple1[0] < tuple2[0] else 'false', 'bool')
            else:
                raise TypeError(f"TypeError: operator '<' cannot compare types '{tuple1[1]}' and '{tuple2[1]}'")
        elif self.value == '>':
            if tuple1[1] == 'i32' and tuple2[1] == 'i32':
                 return ('true' if tuple1[0] > tuple2[0] else 'false', 'bool')
            elif tuple1[1] == 'str' and tuple2[1] == 'str':
                 return ('true' if tuple1[0] > tuple2[0] else 'false', 'bool')
            else:
                raise TypeError(f"TypeError: operator '>' cannot compare types '{tuple1[1]}' and '{tuple2[1]}'")
        elif self.value == '++':
            val1_str = str(tuple1[0])
            val2_str = str(tuple2[0])
            return (val1_str + val2_str, 'str')

class UnOp(Node):
    def Evaluate(self, st):
        val_tuple = self.children[0].Evaluate(st)
        val = val_tuple[0]
        tipo = val_tuple[1]
        if self.value == '!':
            if tipo != 'bool':
                raise TypeError("TypeError: '!' only supports bool")
            py_bool = True if val == 'true' else False
            return ('true' if not py_bool else 'false', 'bool')
        elif self.value == '-':
            if tipo != 'i32':
                raise TypeError("TypeError: unary '-' only supports i32")
            return (-val, 'i32')
        elif self.value == '+':
            if tipo != 'i32':
                raise TypeError("TypeError: unary '+' only supports i32")
            return (val, 'i32')

class While(Node):
     def Evaluate(self, st):
        propagated_return_value = (None, "void")
        while True:
            cond = self.children[0].Evaluate(st)
            if cond[1] != 'bool':
                raise TypeError("TypeError: while condition must be bool")
            cond_bool = True if cond[0] == 'true' else False
            if not cond_bool:
                break
            block_result = self.children[1].Evaluate(st)
            if block_result is not None and block_result[1] != "void":
                propagated_return_value = block_result
                break
        return propagated_return_value

class If(Node):
    def Evaluate(self, st):
        propagated_return_value = (None, "void")
        cond = self.children[0].Evaluate(st)
        if cond[1] != 'bool':
            raise TypeError("TypeError: if condition must be bool")
        cond_bool = True if cond[0] == 'true' else False
        if cond_bool:
            block_result = self.children[1].Evaluate(st)
            if block_result is not None and block_result[1] != "void":
                propagated_return_value = block_result
        elif len(self.children) > 2:
            block_result = self.children[2].Evaluate(st)
            if block_result is not None and block_result[1] != "void":
                propagated_return_value = block_result
        return propagated_return_value

class Read(Node):
    def Evaluate(self, st):
        try:
            return (int(input()), 'i32')
        except ValueError:
            raise ValueError("Input must be an integer for reader()")

class Block(Node):
    def Evaluate(self, st):
        final_return_value = (None, "void")
        for child in self.children:
            evaluated_value = None
            if isinstance(child, Block):
                 st_nested = SymbolTable({}, st)
                 evaluated_value = child.Evaluate(st_nested)
            else:
                 evaluated_value = child.Evaluate(st)
            if evaluated_value is not None and evaluated_value[1] != "void":
                 final_return_value = evaluated_value
                 break
        return final_return_value

class Assignment(Node):
    def Evaluate(self, st):
        key = self.children[0].value
        value_tuple = self.children[1].Evaluate(st)
        st.setter(key, value_tuple)
        return (None, "void")

class Identifier(Node):
    def Evaluate(self, st):
        val, tipo, _ = st.getter(self.value)
        return (val, tipo)

class Print(Node):
    def Evaluate(self, st):
        value, type = self.children[0].Evaluate(st)
        print(value)
        return (None, "void")

class IntVal(Node):
    def Evaluate(self, st):
        return (self.value, 'i32')

class BoolVal(Node):
    def Evaluate(self, st):
        return (self.value, 'bool')

class StrVal(Node):
    def Evaluate(self, st):
        return (self.value, 'str')

class VarDec(Node):
    def Evaluate(self, st):
        var_name = self.children[0].value
        declared_type = self.value
        if len(self.children) == 1:
            st.create_variable(var_name, None, declared_type, False)
        else:
            init_value_tuple = self.children[1].Evaluate(st)
            st.create_variable(var_name, init_value_tuple, declared_type, False)
        return (None, "void")

class NoOp(Node):
    def Evaluate(self, st):
        return (None, "void")

class FuncDec(Node):
    def __init__(self, value, children, returnType):
       super().__init__(value, children)
       self.returnType = returnType
    @property
    def block(self):
       return self.children[-1]
    def Evaluate(self, st):
        st.create_variable(self.value, self, self.returnType, True)
        return (None, "void")

class FuncCall(Node):
    def Evaluate(self, st):
        val, tipo_retorno_declarado, isFunc = st.getter(self.value)

        if not isFunc:
            raise TypeError(f"'{self.value}' is not a function")
        func_dec_node = val
        num_params_declarados = len(func_dec_node.children) - 1
        num_args_passados = len(self.children)
        if num_args_passados != num_params_declarados:
            raise ValueError(f"Argument count mismatch for function '{self.value}': expected {num_params_declarados}, got {num_args_passados}")
        local_st = SymbolTable({}, st)
        for i in range(num_args_passados):
            param_decl = func_dec_node.children[i]
            param_name = param_decl.children[0].value
            param_type = param_decl.value
            arg_val = self.children[i].Evaluate(st)

            if arg_val[1] != param_type:
                 if not (arg_val[1] == 'bool' and param_type == 'bool'):
                      raise TypeError(f"TypeError: Argument {i} ('{param_name}') for function '{self.value}' expected type '{param_type}' but got '{arg_val[1]}'")
            try:
                local_st.create_variable(param_name, arg_val, param_type, False)
                #print(f"[DEBUG] ST de '{self.value}' após criar param '{param_name}': {local_st.symbols}")
            except Exception as e:
                 raise RuntimeError(f"Error creating parameter '{param_name}' in function '{self.value}': {e}")
        #print(f"[DEBUG] ST local final de '{self.value}' antes da execução do bloco: {local_st.symbols}")
        result = func_dec_node.block.Evaluate(local_st)
        #print(f"[DEBUG] Retorno de {self.value}: {result}")
        retorno_declarado = func_dec_node.returnType
        tipo_retornado = result[1] if result is not None else "void"
        if retorno_declarado == "void" and tipo_retornado != "void":
             raise TypeError(f"TypeError: Function '{self.value}' declared as void returned a value of type '{tipo_retornado}'")
        if retorno_declarado != "void" and tipo_retornado == "void":
             raise TypeError(f"TypeError: Function '{self.value}' declared to return '{retorno_declarado}' did not return a value (returned void)")
        if retorno_declarado != "void" and tipo_retornado != "void":
             if not (retorno_declarado == 'bool' and tipo_retornado == 'bool'):
                 if tipo_retornado != retorno_declarado:
                     raise TypeError(f"TypeError: Function '{self.value}' declared to return '{retorno_declarado}' returned incompatible type '{tipo_retornado}'")
        return result

class Return(Node):
    def Evaluate(self, st):
        return self.children[0].Evaluate(st)