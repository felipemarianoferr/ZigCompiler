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
            
            else:
                raise Exception("Error")
        
class Parser:

    tokenizer = None

    def parseTerm():
        if Parser.tokenizer.next.tipoToken == 'INT':
            resultado = Parser.tokenizer.next.valorToken
            Parser.tokenizer.selectNext()
            while Parser.tokenizer.next.tipoToken in ['DIV', 'MULT']:
                if Parser.tokenizer.next.tipoToken == 'DIV':
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.tipoToken == 'INT' and Parser.tokenizer.next.valorToken != 0:
                        resultado = resultado // Parser.tokenizer.next.valorToken
                    else:
                        raise Exception ("Error")
                if Parser.tokenizer.next.tipoToken == 'MULT':
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.tipoToken == 'INT':
                        resultado *= Parser.tokenizer.next.valorToken
                    else:
                        raise Exception ("Error")
                Parser.tokenizer.selectNext()
            return resultado
        raise Exception ("Error")

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
            raise Exception ("Error")
        return resultado

if __name__ == "__main__":
    source = sys.argv[1]
    print(Parser.run(source))