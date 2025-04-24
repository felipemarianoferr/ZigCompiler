from compiler.Ast import *
from compiler.Tokenizer import Tokenizer
from compiler.SymbolTable import SymbolTable
from compiler.PrePro import PrePro

class Parser:

    tokenizer = None

    def parseProgram():
        block = Block('Block', [])
        while Parser.tokenizer.next.tipoToken != 'EOF':
            if Parser.tokenizer.next.tipoToken == 'var':
                block.children.append(Parser.parseVarDec())
                Parser.tokenizer.selectNext()
            elif Parser.tokenizer.next.tipoToken == 'fn':
                block.children.append(Parser.parseFunction())
                Parser.tokenizer.selectNext()
        return block
            
    def parseVarDec():
        if Parser.tokenizer.next.tipoToken == 'var':
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.tipoToken == 'identifier':
                identifier = Identifier(Parser.tokenizer.next.valorToken, [])
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.tipoToken != 'colon':
                    raise Exception('Expected ":"')
                Parser.tokenizer.selectNext()

                if Parser.tokenizer.next.tipoToken not in ['i32', 'bool', 'str', 'void']:
                    raise Exception('Expected type after ":"')
                
                var_type = Parser.tokenizer.next.valorToken
                Parser.tokenizer.selectNext()

                if Parser.tokenizer.next.tipoToken == 'assignment':
                    Parser.tokenizer.selectNext()
                    ast_node = Parser.parseBoolExpression()
                    if Parser.tokenizer.next.tipoToken != 'semi_colon':
                        raise Exception('Expected ";"')
                    Parser.tokenizer.selectNext()
                    var_decl = VarDec(var_type, [])
                    var_decl.children.append(identifier)
                    var_decl.children.append(ast_node)
                    return var_decl
                else:
                    var_decl = VarDec(var_type, [])
                    var_decl.children.append(identifier)
                    if Parser.tokenizer.next.tipoToken != 'semi_colon':
                        raise Exception('Expected ";"')
                    Parser.tokenizer.selectNext()
                    return var_decl
            else:
                raise Exception('Expected identifier after "var"')

    def parseFunction():
        if Parser.tokenizer.next.tipoToken == 'fn':
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.tipoToken == 'identifier':
                funcDec = FuncDec(Parser.tokenizer.next.valorToken, [], None)
                funcDec.children.append(Parser.tokenizer.next.valorToken)
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.tipoToken == 'OPEN':
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.tipoToken == 'CLOSE':
                        Parser.tokenizer.selectNext()
                        if Parser.tokenizer.next.tipoToken in ['i32', 'bool', 'str', 'void']:
                            funcDec.returnType = Parser.tokenizer.next.valorToken
                            funcDec.children.append(Parser.parseBlock)
                            return funcDec
                    elif Parser.tokenizer.next.tipoToken == 'identifier':
                        while Parser.tokenizer.next.tipoToken != 'CLOSE':
                            if Parser.tokenizer.next.tipoToken == 'identifier':
                                identifier = Identifier(Parser.tokenizer.next.valorToken, [])
                                Parser.tokenizer.selectNext()
                                if Parser.tokenizer.next.tipoToken != 'colon':
                                    raise Exception('Expected ":"')
                                Parser.tokenizer.selectNext()

                                if Parser.tokenizer.next.tipoToken not in ['i32', 'bool', 'str', 'void']:
                                    raise Exception('Expected type after ":"')
                                
                                var_type = Parser.tokenizer.next.valorToken
                                Parser.tokenizer.selectNext()

                                if Parser.tokenizer.next.valorToken not in [',', ')']:
                                    raise Exception('Expected "," or ")"')
                                
                                var_decl = VarDec(var_type, [])
                                var_decl.children.append(identifier)
                                funcDec.children.append(var_decl)

                                Parser.tokenizer.selectNext()
                            else:
                                raise Exception('Expected identifier')
                        Parser.tokenizer.selectNext()
                        if Parser.tokenizer.next.tipoToken in ['i32', 'bool', 'str', 'void']:
                            funcDec.returnType = Parser.tokenizer.next.valorToken
                            funcDec.children.append(Parser.parseBlock)
                            return funcDec
                        else:
                            raise Exception('Expected type')   
                    else:
                        raise Exception('Expected ")" or identifier')
            else:
                raise Exception('Expected identifier after "fn"')
                
        else:
            raise Exception('Expected "fn"')

    def parseTerm():
        ast_node = Parser.parseFactor()
        while Parser.tokenizer.next.tipoToken in ['MULT', 'DIV', 'concat']:
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
            elif Parser.tokenizer.next.tipoToken == 'concat':
                Parser.tokenizer.selectNext()
                bin_op = BinOp('++', [])
                bin_op.children.append(ast_node)
                bin_op.children.append(Parser.parseFactor())
                ast_node = bin_op

        return ast_node
    
    def parseBoolTerm():
        ast_node = Parser.parseRedExpression()
        while Parser.tokenizer.next.tipoToken in ['and']:
            if Parser.tokenizer.next.tipoToken == 'and':
                Parser.tokenizer.selectNext()
                bin_op = BinOp('&&', [])
                bin_op.children.append(ast_node)
                bin_op.children.append(Parser.parseExpression())
                ast_node = bin_op
        return ast_node

    def parseBoolExpression():
        ast_node = Parser.parseBoolTerm()
        while Parser.tokenizer.next.tipoToken in ['or']:
            if Parser.tokenizer.next.tipoToken == 'or':
                Parser.tokenizer.selectNext()
                bin_op = BinOp('||', [])
                bin_op.children.append(ast_node)
                bin_op.children.append(Parser.parseBoolTerm())
                ast_node = bin_op
        return ast_node
    
    def parseRedExpression():
        ast_note = Parser.parseExpression()
        while Parser.tokenizer.next.tipoToken in ['equal', 'less', 'greater']:
            if Parser.tokenizer.next.tipoToken == 'equal':
                Parser.tokenizer.selectNext()
                bin_op = BinOp('==', [])
                bin_op.children.append(ast_note)
                bin_op.children.append(Parser.parseExpression())
                ast_note = bin_op
            elif Parser.tokenizer.next.tipoToken == 'less':
                Parser.tokenizer.selectNext()
                bin_op = BinOp('<', [])
                bin_op.children.append(ast_note)
                bin_op.children.append(Parser.parseExpression())
                ast_note = bin_op
            elif Parser.tokenizer.next.tipoToken == 'greater':
                Parser.tokenizer.selectNext()
                bin_op = BinOp('>', [])
                bin_op.children.append(ast_note)
                bin_op.children.append(Parser.parseExpression())
                ast_note = bin_op
        return ast_note

    def parseFactor():

        if Parser.tokenizer.next.tipoToken == 'INT':
            value = Parser.tokenizer.next.valorToken
            int_val = IntVal(value,[])
            Parser.tokenizer.selectNext()
            return int_val
        
        elif Parser.tokenizer.next.tipoToken == 'bool':
            if Parser.tokenizer.next.valorToken == 'true':
                value = True
            else:
                value = False
            bool_val = BoolVal(value, [])
            Parser.tokenizer.selectNext()
            return bool_val
        
        elif Parser.tokenizer.next.tipoToken == 'str':
            value = Parser.tokenizer.next.valorToken
            str_val = StrVal(value, [])
            Parser.tokenizer.selectNext()
            return str_val
        
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

        elif Parser.tokenizer.next.tipoToken == 'not':
            Parser.tokenizer.selectNext()
            un_op  = UnOp('!', [])
            un_op.children.append(Parser.parseFactor())
            return un_op

        elif Parser.tokenizer.next.tipoToken == 'OPEN':
            Parser.tokenizer.selectNext()
            result = Parser.parseBoolExpression()
            if Parser.tokenizer.next.tipoToken == 'CLOSE':
                Parser.tokenizer.selectNext()
                return result
            else:
                raise Exception ("Parenthesis not detected")
            
        elif Parser.tokenizer.next.tipoToken == 'read':
            Parser.tokenizer.selectNext()
            read = Read('read', [])
            if Parser.tokenizer.next.tipoToken == 'OPEN':
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.tipoToken == 'CLOSE':
                    Parser.tokenizer.selectNext()
                    return read
                else:
                    raise Exception ("Parenthesis not detected")
            else:
                raise Exception ("Expected '('")
            
        elif Parser.tokenizer.next.tipoToken == 'identifier':
            identifier = Identifier(Parser.tokenizer.next.valorToken, [])
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.tipoToken == 'OPEN':
                funcCall = FuncCall(identifier.value, [])
                Parser.tokenizer.selectNext()
                while Parser.tokenizer.next.tipoToken != 'CLOSE':
                    funcCall.children.append(Parser.parseBoolExpression())
                    if Parser.tokenizer.next.valorToken == ',':
                        Parser.tokenizer.selectNext()
                    elif Parser.tokenizer.next.tipoToken == 'CLOSE':
                        pass
                    else:
                        raise Exception('Expected "," or ")"')
                Parser.tokenizer.selectNext()
                return funcCall
            
            else:
                raise Exception(f'To call a function, identifier must be followed by "("')
            
        else:
            raise Exception (f"symbol {Parser.tokenizer.next.tipoToken} not recognized")

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
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.tipoToken == 'assignment':
                assignment = Assignment('assignment', [])
                assignment.children.append(identifier)
                Parser.tokenizer.selectNext()
                ast_node = Parser.parseBoolExpression()
                if Parser.tokenizer.next.tipoToken != 'semi_colon':
                    raise Exception('Expected ";"')
                Parser.tokenizer.selectNext()
                assignment.children.append(ast_node)
                return assignment
            elif Parser.tokenizer.next.tipoToken == 'OPEN':
                funcCall = FuncCall(identifier.value, [])
                Parser.tokenizer.selectNext()
                while Parser.tokenizer.next.tipoToken != 'CLOSE':
                    funcCall.children.append(Parser.parseBoolExpression())
                    if Parser.tokenizer.next.valorToken == ',':
                        Parser.tokenizer.selectNext()
                    elif Parser.tokenizer.next.tipoToken == 'CLOSE':
                        pass
                    else:
                        raise Exception('Expected "," or ")"')
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.tipoToken != 'semi_colon':
                    raise Exception('Expected ";"')
                return funcCall
        
            else:
                raise Exception(f'Identifiers must be followed by "=" or "("')
        
        elif Parser.tokenizer.next.tipoToken == 'print':
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.tipoToken == 'OPEN':
                Parser.tokenizer.selectNext()
                ast_node = Parser.parseBoolExpression()
                if Parser.tokenizer.next.tipoToken == 'CLOSE':
                    Parser.tokenizer.selectNext()
                else:
                    raise Exception('Expected ")"')
                if Parser.tokenizer.next.tipoToken != 'semi_colon':
                    raise Exception('Expected ";"')
                Parser.tokenizer.selectNext()
                pnt = Print('print', [])
                pnt.children.append(ast_node)
            else:
                raise Exception('Expected "("')
            return pnt
        
        elif Parser.tokenizer.next.tipoToken == 'while':
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.tipoToken == 'OPEN':
                Parser.tokenizer.selectNext()
            else:
                raise Exception('Expected "("')
            ast_node = Parser.parseBoolExpression()
            if Parser.tokenizer.next.tipoToken == 'CLOSE':
                Parser.tokenizer.selectNext()
            else:
                raise Exception('Expected ")"')
            # Parser.tokenizer.selectNext()
            wle = While('while', [])
            wle.children.append(ast_node)
            wle.children.append(Parser.parseBlock())
            return wle
        
        elif Parser.tokenizer.next.tipoToken == 'if':
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.tipoToken == 'OPEN':
                Parser.tokenizer.selectNext()
            else:
                raise Exception('Expected "("')
            ast_node = Parser.parseBoolExpression()
            if Parser.tokenizer.next.tipoToken == 'CLOSE':
                Parser.tokenizer.selectNext()
            else:
                raise Exception('Expected ")"')
            # Parser.tokenizer.selectNext()
            if_node = If('if', [])
            if_node.children.append(ast_node)
            if_node.children.append(Parser.parseBlock())
            if Parser.tokenizer.next.tipoToken == 'else':
                Parser.tokenizer.selectNext()
                if_node.children.append(Parser.parseBlock())
            return if_node

        elif Parser.tokenizer.next.tipoToken == 'RETURN':
            Parser.tokenizer.selectNext()
            ast_node = Parser.parseBoolExpression()
            if Parser.tokenizer.next.tipoToken != 'semi_colon':
                raise Exception('Expected ";"')
            Parser.tokenizer.selectNext()
            return Return('return', [ast_node])
        
        elif Parser.tokenizer.next.tipoToken == 'open_curly_brace':
            return Parser.parseBlock()
        
        elif Parser.tokenizer.next.tipoToken == 'var':
            return Parser.parseVarDec()
        
        else:
            raise Exception('Expected statement')

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
        ast_node = Parser.parseProgram()
        main_call = FuncCall("main", [])
        ast_node.children.append(main_call)
        if Parser.tokenizer.next.tipoToken != 'EOF':
            raise Exception ("Unconsumed tokens")
        return ast_node.Evaluate(st)