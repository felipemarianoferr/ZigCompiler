from compiler.Code import Code
class Node():
    id = 0
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.increment_id()

    def Evaluate(self, st):
        pass
    
    def generate(self, st):
        pass

    def increment_id():
        Node.id += 1
        return Node.id

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
        
    def generate(self, st):
        self.children[1].generate(st)  # resultado em eax
        Code.append("push eax")
        self.children[0].generate(st)  # resultado em eax
        Code.append("pop ecx")

        if self.value == '+':
            Code.append("add eax, ecx")
        elif self.value == '-':
            Code.append("sub eax, ecx")
        elif self.value == '*':
            Code.append("imul eax, ecx")
        elif self.value == '/':
            Code.append("xchg eax, ecx")
            Code.append("cdq")
            Code.append("idiv ecx")
        elif self.value == '==':
            Code.append("cmp eax, ecx")
            Code.append("mov eax, 0")
            Code.append("mov ecx, 1")
            Code.append("cmove eax, ecx")
        elif self.value == '>':
            Code.append("cmp eax, ecx")
            Code.append("mov eax, 0")
            Code.append("mov ecx, 1")
            Code.append("cmovg eax, ecx")
        elif self.value == '<':
            Code.append("cmp eax, ecx")
            Code.append("mov eax, 0")
            Code.append("mov ecx, 1")
            Code.append("cmovl eax, ecx")
        elif self.value == '&&':
            Code.append("test eax, eax")
            Code.append("je false_and_" + str(self.id))
            Code.append("test ecx, ecx")
            Code.append("je false_and_" + str(self.id))
            Code.append("mov eax, 1")
            Code.append("jmp end_and_" + str(self.id))
            Code.append("false_and_" + str(self.id) + ":")
            Code.append("mov eax, 0")
            Code.append("end_and_" + str(self.id) + ":")
        elif self.value == '||':
            Code.append("test eax, eax")
            Code.append("jne true_or_" + str(self.id))
            Code.append("test ecx, ecx")
            Code.append("jne true_or_" + str(self.id))
            Code.append("mov eax, 0")
            Code.append("jmp end_or_" + str(self.id))
            Code.append("true_or_" + str(self.id) + ":")
            Code.append("mov eax, 1")
            Code.append("end_or_" + str(self.id) + ":")
        
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
    
    def generate(self, st):
        self.children[0].generate(st)
        if self.value == '!':
            Code.append("cmp eax, 0")
            Code.append("mov eax, 0")
            Code.append("mov ebx, 1")
            Code.append("cmove eax, ecx")
        elif self.value == '-':
            Code.append("neg eax")
        elif self.value == '+':
            pass


class While(Node):
    def Evaluate(self, st):
        cond = self.children[0].Evaluate(st)
        if cond[1] != 'bool':
            raise Exception("TypeError: condition must be bool")
        while cond[0]:
            self.children[1].Evaluate(st)
            cond = self.children[0].Evaluate(st)
    
    def generate(self, st):
        start_label = f"loop_{self.id}"
        end_label = f"exit_{self.id}"

        Code.append(f"{start_label}:")
        self.children[0].generate(st)
        Code.append("cmp eax, 0")
        Code.append(f"je {end_label}")
        self.children[1].generate(st)
        Code.append(f"jmp {start_label}")
        Code.append(f"{end_label}:")

class If(Node):
    def Evaluate(self, st):
            cond = self.children[0].Evaluate(st)
            if cond[1] != 'bool':
                raise Exception("TypeError: condition must be bool")
            if cond[0]:
                self.children[1].Evaluate(st)
            elif len(self.children) > 2:
                self.children[2].Evaluate(st)
    
    def generate(self, st):
        else_label = f"else_{self.id}"
        end_label = f"endif_{self.id}"

        self.children[0].generate(st)
        Code.append("cmp eax, 0")
        Code.append(f"je {else_label}")
        self.children[1].generate(st)
        Code.append(f"jmp {end_label}")
        Code.append(f"{else_label}:")
        if len(self.children) > 2:
            self.children[2].generate(st)
        Code.append(f"{end_label}:")

class Read(Node):
    def Evaluate(self, st):
        return (int(input()), 'i32')

    def generate(self, st):
        Code.append("push scan_int")
        Code.append("push format_in")
        Code.append("call scanf")
        Code.append("add esp, 8")
        Code.append("mov eax, [scan_int]")

class Block(Node):

    def Evaluate(self, st):
        for child in self.children:
            child.Evaluate(st)
    
    def generate(self, st):
        for child in self.children:
            child.generate(st)

class Assignment(Node):

    def Evaluate(self, st):
        key = self.children[0].value
        st.setter(key, self.children[1].Evaluate(st))

    def generate(self, st):
        self.children[1].generate(st)
        offset = st.getter_offset(self.children[0].value)
        Code.append(f"mov [ebp{offset}], eax")

class Identifier(Node):

    def Evaluate(self, st):
        return st.getter(self.value)
    
    def generate(self, st):
        offset = st.getter_offset(self.value)
        Code.append(f"mov eax, [ebp{offset}]")

class Print(Node):

    def Evaluate(self, st):
        value, type = self.children[0].Evaluate(st)
        if type == 'bool':
            value = str(value).lower()
        print(value)
    
    def generate(self, st):
        self.children[0].generate(st)
        Code.append("push eax")
        Code.append("push format_out")
        Code.append("call printf")
        Code.append("add esp, 8")


class IntVal(Node):

    def Evaluate(self, st):
        return (self.value, 'i32')

    def generate(self, st):
        Code.append("mov eax," + str(self.value))

class BoolVal(Node): 
         
    def Evaluate(self, st):
        return (self.value, 'bool')
    
    def generate(self, st):
        Code.append("mov eax, 1" if self.value else "mov eax, 0")
    
class StrVal(Node):

    def Evaluate(self, st):
        return (self.value, 'str')
    
    def generate(self, st):
        pass
    
class VarDec(Node):

    def Evaluate(self, st):
        if (len(self.children) == 1):
            st.create_variable(self.children[0].value, None, self.value)
        else:
            st.create_variable(self.children[0].value, self.children[1].Evaluate(st), self.value)

    def generate(self, st):
        st.create_variable(self.children[0].value, None, self.value)
        offset = st.getter_offset(self.children[0].value)
        Code.append("sub esp, 4")
        if len(self.children) > 1:
            self.children[1].generate(st)
            Code.append(f"mov [ebp{offset}], eax")
            
    
class NoOp(Node):

    def Evaluate(self, st):
        return (None, None)
    
    def generate(self, st):
        pass