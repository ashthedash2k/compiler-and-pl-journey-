
'''
TO ADD: 
- keywords
- comments
- lol fix error message
- boolean (true false, and or ?)
- line and column tracking
'''

class Error:
    def __init__(self, pos):
        self.pos = pos

class Lexer:
    def __init__(self, input_data):
        self.input = input_data
        self.position = 0
        self.tokens = []
        self.type = ''
    def next_char(self):
        if self.position + 1 < len(self.input):
            return self.input[self.position + 1]
        return ''

    def tokenize(self):
        while self.position < len(self.input):
            char = self.input[self.position]
            if char in [' ', '\t', '\n', '\r']:
                self.position += 1
            elif char in ['"', "'"]: 
                string_value = self.read_string(char)
                self.tokens.append(('STRING', string_value, self.position))
            elif char == '=' and self.next_char() == '=':
                self.tokens.append(('EQUALS (bool)', '==', self.position))
                self.position += 2
            elif char == '!' and self.next_char() == '=':
                self.tokens.append(('NOT EQUAL (bool)', '!=', self.position))
                self.position += 2
            elif char == '<' and self.next_char() == '=':
                self.tokens.append(('LESS THAN EQUAL', '<=', self.position))
                self.position += 2
            elif char == '>' and self.next_char() == '=':
                self.tokens.append(('GREATER THAN EQUAL', '>=', self.position))
                self.position += 2
            elif char == '=':
                self.tokens.append(('EQUALS (assignment)', char, self.position))
                self.position += 1
            elif char == '-':
                self.tokens.append(('MINUS', char, self.position))
                self.position += 1
            elif char == '%':
                self.tokens.append(('MOD', char, self.position))
                self.position += 1
            elif char == '<':
                self.tokens.append(('LESS THAN', char, self.position))
                self.position += 1
            elif char == '>':
                self.tokens.append(('GREATER THAN', char, self.position))
                self.position += 1
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
                number_value = self.read_number()
                token_type = 'FLOAT' if '.' in number_value else 'INTEGER'
                self.tokens.append((token_type, number_value, self.position))
            else:
                raise Error(self.position)

        return self.tokens

    # def read_integer(self):
    #     start_position = self.position
    #     while self.position < len(self.input) and self.input[self.position].isdigit():
    #         self.position += 1
    #     return self.input[start_position:self.position]

    def read_number(self):
        start_position = self.position
        while self.position < len(self.input):
            if self.input[self.position].isdigit():
                self.position += 1
            elif self.input[self.position] == '.':
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

data = '4'
lexer = Lexer(data)
tokens = lexer.tokenize()
print(tokens)
