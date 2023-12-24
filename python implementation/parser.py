from lexer import Lexer 

class Parser:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.curr_token = None
        self.next_token()

    def next_token(self):
        self.curr_token = next(self.tokens, None)
    
    def operands(self):
        if self.curr_token and self.curr_token[0] in ['INTEGER', 'FLOAT']:
            result = float(self.curr_token[1]) if self.curr_token[0] == 'FLOAT' else int(self.curr_token[1])
            self.next_token()
        else:
            raise SyntaxError("Expected a number at the beginning of expression")

        while self.curr_token:
            if self.curr_token[0] == 'PLUS':
                self.next_token()
                if self.curr_token[0] in ['INTEGER', 'FLOAT']:
                    result += float(self.curr_token[1]) if self.curr_token[0] == 'FLOAT' else int(self.curr_token[1])
                else:
                    raise SyntaxError("Expected a number after '+'")
            elif self.curr_token[0] == 'MULT':
                self.next_token()
                if self.curr_token[0] in ['INTEGER', 'FLOAT']:
                    result *= float(self.curr_token[1]) if self.curr_token[0] == 'FLOAT' else int(self.curr_token[1])
                else:
                    raise SyntaxError("Expected a number after '*'")
            elif self.curr_token[0] == 'MINUS':
                self.next_token()
                if self.curr_token[0] in ['INTEGER', 'FLOAT']:
                    result -= float(self.curr_token[1]) if self.curr_token[0] == 'FLOAT' else int(self.curr_token[1])
                else:
                    raise SyntaxError("Expected a number after '-'")

            else:
                raise SyntaxError("Unexpected token")

            self.next_token()

        return result



data = "1 + 2 * 3 + 4 - 10"
lexer = Lexer(data)
tokens = lexer.tokenize()
parser = Parser(tokens)
result = parser.operands()
print("Result:", result)  
