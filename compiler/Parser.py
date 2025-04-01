from compiler.Ast import *
from compiler.Tokenizer import Tokenizer
from compiler.SymbolTable import SymbolTable
from compiler.PrePro import PrePro

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