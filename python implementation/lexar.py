
class Error:
    def __init__(self, pos):
        self.pos = pos

class Lexer:
    def __init__(self, input_data):
        self.input = input_data
        self.position = 0
        self.tokens = []

    def tokenize(self):
        while self.position < len(self.input):
            char = self.input[self.position]
            if char in [' ', '\t', '\n', '\r']:
                self.position += 1
            elif char in ['"', "'"]: 
                string_value = self.read_string(char)
                self.tokens.append(('STRING', string_value, self.position))
            elif char == '+':
                self.tokens.append(('PLUS', char, self.position))
                self.position += 1
            elif char == '(':
                self.tokens.append(('LPAREN', char, self.position))
                self.position += 1
            elif char == ')':
                self.tokens.append(('RPAREN', char, self.position))
                self.position += 1
            elif char == '*':
                self.tokens.append(('MULT', char, self.position))
                self.position += 1
            elif char == '/':
                self.tokens.append(('REG DIV', char, self.position))
                self.position += 1
            #lol fix positioning its messed up
            elif char.isdigit():
                self.tokens.append(('INTEGER', self.read_integer(), self.position))
            else:
                raise Error(self.position)

        return self.tokens

    def read_integer(self):
        start_position = self.position
        while self.position < len(self.input) and self.input[self.position].isdigit():
            self.position += 1
        return self.input[start_position:self.position]
    
    def read_string(self, identifier):
        self.position += 1 
        inside_identifier = ""

        while self.position < len(self.input):
            char = self.input[self.position]
            if char == identifier:
                break
            else:
                inside_identifier += char
                self.position += 1
        self.position += 1

        return inside_identifier 




data = '1+2+"hello world"+\'test string\'+3+4/4'
lexer = Lexer(data)
tokens = lexer.tokenize()
print(tokens)
