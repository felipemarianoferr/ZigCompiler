import sys
import re
class Token:
    def __init__(self, tipoToken, valorToken):
        self.tipoToken = tipoToken
        self.valorToken = valorToken

class Node():

    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self):
        pass

class BinOp(Node):

    def Evaluate(self):
        if self.value == '+':
            return self.children[0].Evaluate() + self.children[1].Evaluate()
        elif self.value == '-':
            return self.children[0].Evaluate() - self.children[1].Evaluate()
        elif self.value == '*':
            return self.children[0].Evaluate() * self.children[1].Evaluate()
        elif self.value == '/':
            return self.children[0].Evaluate() // self.children[1].Evaluate()
class UnOp(Node):

    def Evaluate(self):
        if self.value == '-':
            return -self.children[0].Evaluate()
        return self.children[0].Evaluate()

class IntVal(Node):

    def Evaluate(self):
        return self.value
    
class NoOp(Node):

    def Evaluate(self):
        pass

class PrePro:

    regex_comentarios = r"//.*?$"

    def filter(source):
        return re.sub(PrePro.regex_comentarios, "", source, flags=re.MULTILINE)

class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None
        self.num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.selectNext()

    def selectNext(self):

        while self.position < len(self.source) and self.source[self.position] == ' ':
            self.position += 1
        if self.position >= len(self.source):
            self.next = Token('EOF','')
            return
        
        if self.position < len(self.source):
            if self.source[self.position] == '+':
                self.next = Token('PLUS', '+')
                self.position += 1
            
            elif self.source[self.position] == '-':
                self.next = Token('MINUS', '-')
                self.position += 1
            
            elif self.source[self.position] == '/':
                self.next = Token('DIV', '/')
                self.position += 1
            
            elif self.source[self.position] == '*':
                self.next = Token('MULT', '*')
                self.position += 1
            
            elif self.source[self.position] in self.num:
                val = self.source[self.position]
                self.position += 1
                while self.position < len(self.source) and self.source[self.position] in self.num:
                    val += self.source[self.position]
                    self.position += 1
                self.next = Token('INT', int(val))

            elif self.source[self.position] == '(':
                self.next = Token('OPEN', '(')
                self.position += 1
            
            elif self.source[self.position] == ')':
                self.next = Token('CLOSE', ')')
                self.position += 1
            
            else:
                raise Exception("Unrecognised letter")
        
class Parser:

    tokenizer = None

    def parseTerm():
        ast_node = Parser.parseFactor()
        while Parser.tokenizer.next.tipoToken in ['MULT', 'DIV']:
            if Parser.tokenizer.next.tipoToken == 'MULT':
                Parser.tokenizer.selectNext()
                bin_op = BinOp('*', [])
                bin_op.children.append(ast_node)
                bin_op.children.append(Parser.parseFactor())
                ast_node = bin_op
            elif Parser.tokenizer.next.tipoToken == 'DIV':
                Parser.tokenizer.selectNext()
                bin_op = BinOp('/', [])
                bin_op.children.append(ast_node)
                bin_op.children.append(Parser.parseFactor())
                ast_node = bin_op
        return ast_node

    def parseFactor():

        if Parser.tokenizer.next.tipoToken == 'INT':
            value = Parser.tokenizer.next.valorToken
            int_val = IntVal(value,[])
            Parser.tokenizer.selectNext()
            return int_val

        elif Parser.tokenizer.next.tipoToken == 'PLUS':
            Parser.tokenizer.selectNext()
            un_op  = UnOp('+', [])
            un_op.children.append(Parser.parseFactor())
            return un_op

        elif Parser.tokenizer.next.tipoToken == 'MINUS':
            Parser.tokenizer.selectNext()
            un_op  = UnOp('-', [])
            un_op.children.append(Parser.parseFactor())
            return un_op

        elif Parser.tokenizer.next.tipoToken == 'OPEN':
            Parser.tokenizer.selectNext()
            result = Parser.parseExpression()
            if Parser.tokenizer.next.tipoToken == 'CLOSE':
                Parser.tokenizer.selectNext()
                return result
            else:
                raise Exception ("Parenthesis not detected")
        else:
            raise Exception ("symbol not recognized")

    def parseExpression():
        ast_node = Parser.parseTerm()
        while Parser.tokenizer.next.tipoToken in ['PLUS', 'MINUS']:
            if Parser.tokenizer.next.tipoToken == 'PLUS':
                Parser.tokenizer.selectNext()
                bin_op = BinOp('+', [])
                bin_op.children.append(ast_node)
                bin_op.children.append(Parser.parseTerm())
                ast_node = bin_op
            elif Parser.tokenizer.next.tipoToken == 'MINUS':
                Parser.tokenizer.selectNext()
                bin_op = BinOp('-', [])
                bin_op.children.append(ast_node)
                bin_op.children.append(Parser.parseTerm())
                ast_node = bin_op
        return ast_node
    

    def run(source):
        source = PrePro.filter(source)
        Parser.tokenizer = Tokenizer(source)
        ast_node = Parser.parseExpression()
        if Parser.tokenizer.next.tipoToken != 'EOF':
            raise Exception ("Unconsumed tokens")
        return ast_node.Evaluate()

if __name__ == "__main__":
    
    source = sys.argv[1]
    try:
        with open(source, "r", encoding="utf-8") as arquivo:
                source = arquivo.read()

    except FileNotFoundError:
        pass

    print(Parser.run(source))