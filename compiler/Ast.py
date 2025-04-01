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
class UnOp(Node):

    def Evaluate(self, st):
        if self.value == '-':
            return -self.children[0].Evaluate(st)
        return self.children[0].Evaluate(st)

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