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
        self.reserverd_variables = ['print', 'if', 'else', 'while', 'reader']
        self.selectNext()

    def selectNext(self):

        while self.position < len(self.source) and self.source[self.position] in (' ', '\n', '\r', '\ufeff', '\t'):
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
                if self.position + 1 < len(self.source) and self.source[self.position + 1] == '=':
                    self.next = Token('equal', '==')
                    self.position += 2
                else:
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
                    if val == 'if':
                        self.next = Token('if', 'if')
                    elif val == 'else':
                        self.next = Token('else', 'else')
                    elif val == 'while':
                        self.next = Token('while', 'while')
                    elif val == 'print':
                        self.next = Token('print', 'print')
                    elif val == 'reader':
                        self.next = Token('read', 'reader')
                else:
                    self.next = Token('identifier', val)

            elif self.source[self.position] == '{':
                self.next = Token('open_curly_brace', '{')
                self.position += 1 

            elif self.source[self.position] == '}':
                self.next = Token('close_curly_brace', '}')
                self.position += 1
            
            elif self.source[self.position] == '|':
                if self.position + 1 < len(self.source) and self.source[self.position + 1] == '|':
                    self.next = Token('or', '||')
                    self.position += 2
            
            elif self.source[self.position] == '&':
                if self.position + 1 < len(self.source) and self.source[self.position + 1] == '&':
                    self.next = Token('and', '&&')
                    self.position += 2
            
            elif self.source[self.position] == '<':
                self.next = Token('less', '<')
                self.position += 1
            
            elif self.source[self.position] == '>':
                self.next = Token('greater', '>')
                self.position += 1
            
            elif self.source[self.position] == '!':
                self.next = Token('not', '!')
                self.position += 1
            
            else:
                raise Exception("Unrecognised letter")