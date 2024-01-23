
'''
lexer.py
@author Ashley C
github: https://github.com/ashthedash2k
email: aczumak@andrew.cmu.edu

This is the compilers lexer, which can currently classify the following tokens: 
- integers
- floats
- sequences of characters
- artihmetic 
- boolean comparrisons 

Features to be implemented: 
- multi line comments
- line and column tracking
- keywords 
- more error handling
'''

class Lexer:
    static_types = ['string', 'float', 'int']
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
            #print(f"Processing character: {char}")
            if char in [' ', '\t', '\n', '\r']:
                self.position += 1
            elif char == '\n':  
                self.tokens.append(('NEWLINE', char))
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
            elif char == '#':
                self.tokens.append(('COMMENT', self.read_sl_comment()))
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
            elif char.isdigit():
                number_value = self.read_number()
                if '.' in number_value:
                    token_type = 'FLOAT'
                else:
                    token_type = 'INTEGER'
                self.tokens.append((token_type, number_value))
            elif char.isalpha() or char == '_':
                identifier = self.read_identifier()
                if identifier in self.static_types:
                    self.tokens.append((f'TYPE_{identifier.upper()}', identifier))
                    self.skip_whitespace()
                    if self.position < len(self.input) and (self.input[self.position].isalpha() or self.input[self.position] == '_'):
                        var_name = self.read_identifier()
                        self.tokens.append(('VARIABLE', var_name))
                elif identifier in self.keywords:
                    self.tokens.append((self.keywords[identifier], identifier))
                elif identifier in self.logic:
                    self.tokens.append((self.logic[identifier], identifier))
                else: 
                    self.tokens.append(('IDENTIFIER', identifier))

            else:
                raise ValueError("cannot parse: ", char)

        return self.tokens
        
    def read_identifier(self):
        start_position = self.position
        while self.position < len(self.input) and (self.input[self.position].isalnum()):
            self.position += 1
        return self.input[start_position:self.position]

    def read_number(self):
        start_position = self.position
        is_dot = False
        while self.position < len(self.input):
            if self.input[self.position].isdigit():
                self.position += 1
            elif self.input[self.position] == '.':
                #need this check for like 1.2.3 or other weird invalid instances
                if is_dot:
                    break
                is_dot = True
                self.position += 1
            else: #break if non character
                break
        return self.input[start_position:self.position]
    
    def read_string(self, quote_type):
        self.position += 1 
        start_position = self.position
        while self.position < len(self.input) and self.input[self.position] != quote_type:
            self.position += 1
        string_literal = self.input[start_position:self.position]
        self.position += 1 
        return string_literal
    
    def skip_whitespace(self):
        while self.position < len(self.input) and self.input[self.position] in [' ', '\t', '\n', '\r']:
            self.position += 1

    
    #single line comments
    def read_sl_comment(self):
        start_position = self.position
        while self.position < len(self.input) and self.input[self.position] != '\n':
            self.position += 1
        return self.input[start_position:self.position]

data = '''int a = 5
string b = "hello"
float c = 3.14'''
lexer = Lexer(data)
tokens = lexer.tokenize()
print(tokens)
