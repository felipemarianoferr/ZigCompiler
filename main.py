import sys

class Token:
    def __init__(self, tipoToken, valorToken):
        self.tipoToken = tipoToken
        self.valorToken = valorToken
        
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
        resultado = Parser.parseFactor()
        while Parser.tokenizer.next.tipoToken in ['MULT', 'DIV']:
            if Parser.tokenizer.next.tipoToken == 'MULT':
                Parser.tokenizer.selectNext()
                mult = Parser.parseFactor()
                resultado *= mult
            elif Parser.tokenizer.next.tipoToken == 'DIV':
                Parser.tokenizer.selectNext()
                div = Parser.parseFactor()
                resultado //= div
        return resultado

    def parseFactor():

        if Parser.tokenizer.next.tipoToken == 'INT':
            value = Parser.tokenizer.next.valorToken
            Parser.tokenizer.selectNext()
            return value

        elif Parser.tokenizer.next.tipoToken == 'PLUS':
            Parser.tokenizer.selectNext()
            return + Parser.parseFactor()

        elif Parser.tokenizer.next.tipoToken == 'MINUS':
            Parser.tokenizer.selectNext()
            return - Parser.parseFactor()

        elif Parser.tokenizer.next.tipoToken == 'OPEN':
            Parser.tokenizer.selectNext()
            result = Parser.parseExpression()
            if Parser.tokenizer.next.tipoToken == 'CLOSE':
                Parser.tokenizer.selectNext()
                return result
            else:
                raise Exception ("Parenthesis ')' not detected")
        else:
            raise Exception


    def parseExpression():
        resultado = Parser.parseTerm()
        while Parser.tokenizer.next.tipoToken in ['PLUS', 'MINUS']:
            if Parser.tokenizer.next.tipoToken == 'PLUS':
                Parser.tokenizer.selectNext()
                soma = Parser.parseTerm()
                resultado += soma
            elif Parser.tokenizer.next.tipoToken == 'MINUS':
                Parser.tokenizer.selectNext()
                sub = Parser.parseTerm()
                resultado -= sub
        return resultado
    

    def run(source):
        Parser.tokenizer = Tokenizer(source)
        resultado = Parser.parseExpression()
        if Parser.tokenizer.next.tipoToken != 'EOF':
            raise Exception ("Unconsumed tokens")
        return resultado

if __name__ == "__main__":
    source = sys.argv[1]
    print(Parser.run(source))