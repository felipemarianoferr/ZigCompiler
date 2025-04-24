from SymbolTable import SymbolTable
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
                raise Exception("TypeError: operator '+' only supports i32")
            
        elif self.value == '-':
            if tuple1[1] == 'i32' and tuple2[1] == 'i32':
                return (tuple1[0] - tuple2[0], 'i32')
            else:
                raise Exception("TypeError: operator '-' only supports i32")
            
        elif self.value == '*':
            if tuple1[1] == 'i32' and tuple2[1] == 'i32':
                return (tuple1[0] * tuple2[0], 'i32')
            else:
                raise Exception("TypeError: operator '*' only supports i32")

        elif self.value == '/':
            if tuple1[1] == 'i32' and tuple2[1] == 'i32':
                return (tuple1[0] // tuple2[0], 'i32')
            else:
                raise Exception("TypeError: operator '/' only supports i32")
            
        elif self.value == '||':
            if tuple1[1] == 'bool' and tuple2[1] == 'bool':
                return (tuple1[0] or tuple2[0], 'bool')
            else:
                raise Exception("TypeError: operator '||' only supports bool, pehaps an type error has occurred during the process")
            
        elif self.value == '&&':
            if tuple1[1] == 'bool' and tuple2[1] == 'bool':
                return (tuple1[0] and tuple2[0], 'bool')
            else:
                raise Exception("TypeError: operator '&&' only supports bool, pehaps an type error has occurred during the process")
            
        elif self.value == '==':
            if tuple1[1] == 'bool' and tuple2[1] == 'bool':
                return (tuple1[0] == tuple2[0], 'bool')
            elif tuple1[1] == 'i32' and tuple2[1] == 'i32':
                return (tuple1[0] == tuple2[0], 'bool')
            elif tuple1[1] == 'str' and tuple2[1] == 'str':
                return (tuple1[0] == tuple2[0], 'bool')
            else:
                raise Exception("TypeError: operator '==' only compares bool, i32 and str, pehaps an type error has occurred during the process")

        elif self.value == '<':
            if tuple1[1] in  'i32' and tuple2[1] == 'i32':
                return (tuple1[0] < tuple2[0], 'bool')
            elif tuple1[1] == 'str' and tuple2[1] == 'str':
                return (tuple1[0] < tuple2[0], 'bool')
            else:
                raise Exception("TypeError: operator '<' only supports i32, pehaps an type error has occurred during the process")
            
        elif self.value == '>':
            if tuple1[1] == 'i32' and tuple2[1] == 'i32':
                return (tuple1[0] > tuple2[0], 'bool')
            elif tuple1[1] == 'str' and tuple2[1] == 'str':
                return (tuple1[0] > tuple2[0], 'bool')
            else:
                raise Exception("TypeError: operator '>' only supports i32, pehaps an type error has occurred during the process")
        elif self.value == '++':
            if (tuple1[1] == 'bool'):
                return (str(tuple1[0]).lower() + str(tuple2[0]), 'str')
            elif(tuple2[1] == 'bool'):
                return (str(tuple1[0]) + str(tuple2[0]).lower(), 'str')
            return (str(tuple1[0]) + str(tuple2[0]), 'str')
        
class UnOp(Node):

    def Evaluate(self, st):
        val, tipo = self.children[0].Evaluate(st)
        if self.value == '!':
            if tipo != 'bool':
                raise Exception("TypeError: '!' only supports bool")
            return (not val, 'bool')
        elif self.value == '-':
            if tipo != 'i32':
                raise Exception("TypeError: unary '-' only supports i32")
            return (-val, 'i32')
        elif self.value == '+':
            if tipo != 'i32':
                raise Exception("TypeError: unary '+' only supports i32")
            return (val, 'i32')


class While(Node):
    def Evaluate(self, st):
        cond = self.children[0].Evaluate(st)
        if cond[1] != 'bool':
            raise Exception("TypeError: condition must be bool")
        while cond[0]:
            self.children[1].Evaluate(st)
            cond = self.children[0].Evaluate(st)

class If(Node):
    def Evaluate(self, st):
            cond = self.children[0].Evaluate(st)
            if cond[1] != 'bool':
                raise Exception("TypeError: condition must be bool")
            if cond[0]:
                self.children[1].Evaluate(st)
            elif len(self.children) > 2:
                self.children[2].Evaluate(st)

class Read(Node):
    def Evaluate(self, st):
        return (int(input()), 'i32')

class Block(Node):

    """ V2.3
     
    def Evaluate(self, st):
        for child in self.children:
          child.Evaluate(st)
    """

    def Evaluate(self, st):
        for child in self.children:
            if child.value == "return":
                returnChild =  child.Evaluate(st)
                if returnChild is not None:
                    return returnChild
                return(None, "void")
            elif child.value == "Block":
                st_child = SymbolTable({}, st)
                returnChild = child.Evaluate(st_child)
                if returnChild is not None:
                    return returnChild
            else:
                child.Evaluate(st)

class Assignment(Node):

    def Evaluate(self, st):
        key = self.children[0].value
        st.setter(key, self.children[1].Evaluate(st))

class Identifier(Node):

    def Evaluate(self, st):
        return st.getter(self.value)

class Print(Node):

    def Evaluate(self, st):
        value, type = self.children[0].Evaluate(st)
        if type == 'bool':
            value = str(value).lower()
        print(value)


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
        if (len(self.children) == 1):
            st.create_variable(self.children[0].value, None, self.value, False)
        else:
            st.create_variable(self.children[0].value, self.children[1].Evaluate(st), self.value, False)
            # if type does not match, raise exception on the create_variable function
    
class NoOp(Node):

    def Evaluate(self, st):
        return (None, None)
    
class FuncDec(Node):

    def __init__(self, value, children, returnType):
        super().__init__(value, children)
        self.returnType = returnType

    def Evaluate(self, st):
        st.create_variable(self.value, self, self.returnType, True)

class FuncCall(Node):

    def Evaluate(self, st):
        func_info = st.getter(self.value)  # busca a função no escopo atual

        # Verifica se é mesmo uma função
        if func_info[2] != True:
            raise Exception(f"'{self.name}' is not a function")

        func_dec_node = func_info[1]  # o nó FuncDec armazenado como valor

        # Verificação do número de argumentos
        if len(self.children) != len(func_dec_node.children) - 2:
            raise Exception("Argument count mismatch")

        local_st = SymbolTable({}, st)

        for i in range(len(self.children)):
            param_decl = func_dec_node.children[i + 1]  # pula o nome
            param_name = param_decl.children[0].value
            param_type = param_decl.value

            arg_val = self.children[i].Evaluate(st)
            local_st.create_variable(param_name, None, param_type, False)
            local_st.setter(param_name, arg_val)

        # Executa corpo da função
        result = func_dec_node.block.Evaluate(local_st)

        # Verifica tipo de retorno
        if result is None and func_dec_node.returnType != "void":
            raise Exception("Function must return a value")
        if result is not None and result[1] != func_dec_node.returnType:
            raise Exception("Function returned wrong type")

        return result

class Return(Node):
    def Evaluate(self, st):
        return self.children[0].Evaluate(st)