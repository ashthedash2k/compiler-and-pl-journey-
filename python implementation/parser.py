from lexer import Lexer 

class Parser:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.curr_token = None
        self.next_token()

    def next_token(self):
        self.curr_token = next(self.tokens, None)
    
    def addition(self):
        result = 0 
        while self.curr_token:
            if self.curr_token[0] in ['INTEGER', 'FLOAT']:
                if self.curr_token[0] == 'FLOAT':
                    result += float(self.curr_token[1])
                elif self.curr_token[0] == 'INTEGER':
                    result += int(self.curr_token[1])
                else:
                    print(f'{self.curr_token[0]} was parsed\n')
                    ValueError('Cannot parse this object')
                self.next_token()
            elif self.curr_token[0] == 'PLUS':
                self.next_token()
            else:
                raise SyntaxError("Unexpected token!")

        return result


data = "1 + 2.5 + 3"
lexer = Lexer(data)
tokens = lexer.tokenize()
parser = Parser(tokens)
result = parser.addition()
print("Result:", result)  
