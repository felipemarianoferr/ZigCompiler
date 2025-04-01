class Node():

    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        pass

class BinOp(Node):

    def Evaluate(self, st):
        if self.value == '+':
            return self.children[0].Evaluate(st) + self.children[1].Evaluate(st)
        elif self.value == '-':
            return self.children[0].Evaluate(st) - self.children[1].Evaluate(st)
        elif self.value == '*':
            return self.children[0].Evaluate(st) * self.children[1].Evaluate(st)
        elif self.value == '/':
            return self.children[0].Evaluate(st) // self.children[1].Evaluate(st)
        elif self.value == '||':
            return self.children[0].Evaluate(st) or self.children[1].Evaluate(st)
        elif self.value == '&&':
            return self.children[0].Evaluate(st) and self.children[1].Evaluate(st)
        elif self.value == '==':
            return self.children[0].Evaluate(st) == self.children[1].Evaluate(st)
        elif self.value == '<':
            return self.children[0].Evaluate(st) < self.children[1].Evaluate(st)
        elif self.value == '>':
            return self.children[0].Evaluate(st) > self.children[1].Evaluate(st)
        
class UnOp(Node):

    def Evaluate(self, st):
        if self.value == '!':
            return not self.children[0].Evaluate(st)
        if self.value == '-':
            return -self.children[0].Evaluate(st)
        return self.children[0].Evaluate(st)

class While(Node):
    def Evaluate(self, st):
        while self.children[0].Evaluate(st):
            self.children[1].Evaluate(st)

class If(Node):
    def Evaluate(self, st):
        if self.children[0].Evaluate(st):
            self.children[1].Evaluate(st)
        elif len(self.children) > 2:
            self.children[2].Evaluate(st)

class Read(Node):
    def Evaluate(self, st):
        return int(input())

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
        print(self.children[0].Evaluate(st))


class IntVal(Node):

    def Evaluate(self, st):
        return self.value
    
class NoOp(Node):

    def Evaluate(self, st):
        return