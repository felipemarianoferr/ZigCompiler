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

    def Evaluate(self, st):
        for child in self.children:
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
            st.create_variable(self.children[0].value, None, self.value)
        else:
            st.create_variable(self.children[0].value, self.children[1].Evaluate(st), self.value)
            # if type does not match, raise exception on the create_variable function
    
class NoOp(Node):

    def Evaluate(self, st):
        return (None, None)