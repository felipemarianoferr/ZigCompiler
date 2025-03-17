import sys
import re
import string
class Token:
    def __init__(self, tipoToken, valorToken):
        self.tipoToken = tipoToken
        self.valorToken = valorToken
class SymbolTable():
    def __init__(self, symbols):
        self.symbols = symbols
    
    def getter(self, key):
        if key in self.symbols:
            return self.symbols[key]
        raise Exception("KeyError")
    
    def setter(self, key, value):
        self.symbols[key] = value
    
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
        self.reserverd_variables = ['print']
        self.selectNext()

    def selectNext(self):

        while self.position < len(self.source) and self.source[self.position] in (' ', '\n', '\r', '\ufeff'):
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
                #gambiarra resolver com professor:
                if self.position < len(self.source) and self.source[self.position].isalpha():
                    raise Exception("Syntax error")
                self.next = Token('INT', int(val))

            elif self.source[self.position] == '(':
                self.next = Token('OPEN', '(')
                self.position += 1
            
            elif self.source[self.position] == ')':
                self.next = Token('CLOSE', ')')
                self.position += 1

            elif self.source[self.position] == '=':
                self.next = Token('assignment', '=')
                self.position += 1

            elif self.source[self.position] == ';':
                self.next = Token('semi_colon', ';')
                self.position += 1

            elif self.source[self.position].isalpha():
                val = ''
                val += self.source[self.position]
                self.position += 1
                while self.source[self.position].isalnum() or self.source[self.position] == '_':
                    val  += self.source[self.position]
                    self.position += 1
                if val in self.reserverd_variables:
                    self.next = Token('print', 'print')
                else:
                    self.next = Token('identifier', val)

            elif self.source[self.position] == '{':
                self.next = Token('open_curly_brace', '{')
                self.position += 1 

            elif self.source[self.position] == '}':
                self.next = Token('close_curly_brace', '}')
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
        
        elif Parser.tokenizer.next.tipoToken == 'identifier':
            value = Parser.tokenizer.next.valorToken
            identifier = Identifier(value, [])
            Parser.tokenizer.selectNext()
            return identifier

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

    def parseBlock():

        if Parser.tokenizer.next.tipoToken == 'open_curly_brace':
            Parser.tokenizer.selectNext()
            block = Block('Block', [])
            while Parser.tokenizer.next.tipoToken != 'close_curly_brace':
                #gambiarra resolver com professor:
                if Parser.tokenizer.next.tipoToken == 'EOF':
                    raise Exception('Expected "}"')
                child = Parser.parseStatement()
                block.children.append(child)

            Parser.tokenizer.selectNext()
            if len(block.children) == 0:
                return NoOp('NoOp', [])
            
            return block
        
        raise Exception('Program must starts with "{"')

    def parseStatement():

        if Parser.tokenizer.next.tipoToken == 'semi_colon':
            Parser.tokenizer.selectNext()
            return NoOp('NoOp', [])
        
        #gambiarra resolver com professor:
        if Parser.tokenizer.next.tipoToken == 'INT':
            raise Exception('Variables cannot start with numbers')
        
        if Parser.tokenizer.next.tipoToken == 'identifier':
            identifier = Identifier(Parser.tokenizer.next.valorToken, [])
            assignment = Assignment('assignment', [])
            assignment.children.append(identifier)
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.tipoToken == 'assignment':
                Parser.tokenizer.selectNext()
                ast_node = Parser.parseExpression()
                if Parser.tokenizer.next.tipoToken != 'semi_colon':
                    raise Exception('Expected ";"')
                Parser.tokenizer.selectNext()
                assignment.children.append(ast_node)
                return assignment
            else:
                raise Exception('Variables must be followed by "="')
        
        if Parser.tokenizer.next.tipoToken == 'print':
            Parser.tokenizer.selectNext()
            ast_node = Parser.parseExpression()
            if Parser.tokenizer.next.tipoToken != 'semi_colon':
                raise Exception('Expected ";"')
            Parser.tokenizer.selectNext()
            pnt = Print('print', [])
            pnt.children.append(ast_node)
            return pnt

        return NoOp('NoOp', [])

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
        st = SymbolTable({})
        ast_node = Parser.parseBlock()
        if Parser.tokenizer.next.tipoToken != 'EOF':
            raise Exception ("Unconsumed tokens")
        return ast_node.Evaluate(st)

if __name__ == "__main__":

    source = sys.argv[1]

    try:
        with open(source, "r") as arquivo:
            code = arquivo.read()
    except FileNotFoundError:
        code = source
   
    # codigo_fonte = """ 
    # {
    # 1x = 1;
    # print(x);
    # }
    # """
    
    Parser.run(code)