from lexer import Lexer 

class Parser:
    def __init__(self, input_data):
        self.lexer = Lexer(input_data)
        self.tokens = iter(self.lexer.tokenize())