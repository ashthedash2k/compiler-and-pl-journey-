
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
            elif char == '//':
                self.tokens.append(('FLOOR DIV', char))
                self.position += 1
            elif char.isdigit():
                self.tokens.append(('INTEGER', self.read_integer()))
            else:
                raise Exception(f"Illegal character: {char}")

        return self.tokens

    def read_integer(self):
        start_position = self.position
        while self.position < len(self.input) and self.input[self.position].isdigit():
            self.position += 1
        return self.input[start_position:self.position]


data = "hi"
lexer = Lexer(data)
tokens = lexer.tokenize()
print(tokens)
