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
        self.num = ['0', '1', '2', '3', '4', '5 ', '6', '7', '8', '9']

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
            
            elif self.source[self.position] in self.num:
                val = self.source[self.position]
                self.position += 1
                while self.position < len(self.source) and self.source[self.position] in self.num:
                    val += self.source[self.position]
                    self.position += 1
                self.next = Token('INT', int(val))
            
            elif self.source[self.position] not in self.num \
                and self.source[self.position] not in [' ', '+', '-']:
                    raise Exception("Erro")
        
class Parser:

    tokenizer = None

        
    def parseExpression():

        sum = 0
        lastType = Parser.tokenizer.next.tipoToken
        lastValue = Parser.tokenizer.next.valorToken
        if lastType == 'INT':
            sum += lastValue
            Parser.tokenizer.selectNext()
        else:
            raise Exception("Error")
            
        while Parser.tokenizer.next.tipoToken != "EOF":

            if Parser.tokenizer.next.tipoToken in ['PLUS', 'MINUS']:
                if lastType != 'INT':
                    raise Exception("Error")

            elif Parser.tokenizer.next.tipoToken == 'INT':
                if lastType == 'PLUS':
                    sum += Parser.tokenizer.next.valorToken
                elif lastType == 'MINUS':
                    sum -= Parser.tokenizer.next.valorToken
                else:
                    raise Exception("Error")

            lastType = Parser.tokenizer.next.tipoToken
            lastValue = Parser.tokenizer.next.valorToken
            Parser.tokenizer.selectNext()
        
        if Parser.tokenizer.next.tipoToken == 'EOF' and lastType != 'INT':
            raise Exception("Error")

        return sum

    def run(source):
        Parser.tokenizer = Tokenizer(source)
        Parser.tokenizer.selectNext()
        return Parser.parseExpression()

if __name__ == "__main__":
    source = sys.argv[1]
    print(Parser.run(source))
