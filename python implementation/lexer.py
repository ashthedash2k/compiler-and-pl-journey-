
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
        #NOT ALL THE POSSIBLE KEYWORDS THAT EXIST IN PYTHON
        self.keywords = {'if': 'IF','elif': 'ELIF', 'else': 'ELSE', 'return': 'RETURN', 'for' : 'FOR LOOP', 'while' : 'WHILE LOOP', 'def' : 'FUNCTION DECLARATION', 
                         'class' : 'CLASS DECLARATION', 'in' : 'IN', 'global' : 'GLOBAL VARIABLE', 'assert' : 'ASSERT STATEMENT'}
        self.logic = {'True': 'TRUE', 'False': 'FALSE', 'and' : 'AND', 'or' : 'OR', 'not' : 'NOT'}
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
                self.tokens.append(('STRING', string_value))
            elif char == '=' and self.next_char() == '=':
                self.tokens.append(('EQUALS (bool)', '=='))
                self.position += 2
            elif char == '!' and self.next_char() == '=':
                self.tokens.append(('NOT EQUAL (bool)', '!='))
                self.position += 2
            elif char == '<' and self.next_char() == '=':
                self.tokens.append(('LESS THAN EQUAL', '<='))
                self.position += 2
            elif char == '>' and self.next_char() == '=':
                self.tokens.append(('GREATER THAN EQUAL', '>='))
                self.position += 2
            elif char == '=':
                self.tokens.append(('EQUALS (assignment)', char))
                self.position += 1
            elif char == '-':
                self.tokens.append(('MINUS', char))
                self.position += 1
            elif char == '%':
                self.tokens.append(('MOD', char))
                self.position += 1
            elif char == '<':
                self.tokens.append(('LESS THAN', char))
                self.position += 1
            elif char == '>':
                self.tokens.append(('GREATER THAN', char))
                self.position += 1
            elif char == '+':
                self.tokens.append(('PLUS', char))
                self.position += 1
            elif char == '(':
                self.tokens.append(('LPAREN', char))
                self.position += 1
            elif char == ')':
                self.tokens.append(('RPAREN', char))
                self.position += 1
            elif char == '*':
                self.tokens.append(('MULT', char))
                self.position += 1
            elif char == '/':
                self.tokens.append(('REG DIV', char))
                self.position += 1
            #lol fix positioning its messed up
            elif char.isdigit():
                number_value = self.read_number()
                token_type = 'FLOAT' if '.' in number_value else 'INTEGER'
                self.tokens.append((token_type, number_value))
            elif char.isalpha() or char == '_':
                identifier = self.read_identifier()
                if identifier in self.keywords:
                    self.tokens.append((self.keywords[identifier], identifier))
                elif identifier in self.logic:
                    self.tokens.append((self.logic[identifier], identifier))
                else: 
                    self.tokens.append(('STRING', identifier))

            else:
                raise Error(self.position)

        return self.tokens
    
    def read_identifier(self):
        start_position = self.position
        while self.position < len(self.input) and (self.input[self.position].isalnum() or self.input[self.position] == '_'):
            self.position += 1
        return self.input[start_position:self.position]

    def read_number(self):
        start_position = self.position
        while self.position < len(self.input):
            if self.input[self.position].isdigit():
                self.position += 1
            elif self.input[self.position] == '.':
                self.position += 1
        return self.input[start_position:self.position]

data = 'for True hey if 1222'
lexer = Lexer(data)
tokens = lexer.tokenize()
print(tokens)
