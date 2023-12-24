from lexer import Lexer
class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value  
        self.left = left   
        self.right = right  

class Parser:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.current_token = None
        self.next_token()

    def next_token(self):
        self.current_token = next(self.tokens, None)

    def parse(self):
        return self.plus_minus()

    def plus_minus(self):
        node = self.mult_div()
        while self.current_token and self.current_token[0] in ['PLUS', 'MINUS']:
            op = self.current_token[0]
            self.next_token()
            right_node = self.mult_div()
            node = Node(op, node, right_node)
        return node

    def mult_div(self):
        node = self.breakdown()
        while self.current_token and self.current_token[0] in ['MULT', 'DIV']:
            op = self.current_token[0]
            self.next_token()
            right_node = self.breakdown()
            node = Node(op, node, right_node)
        return node

    def breakdown(self):
        if self.current_token and self.current_token[0] in ['INTEGER', 'FLOAT']:
            if self.current_token[0] == 'FLOAT':
                value = float(self.current_token[1])
            elif self.current_token[0] == 'INTEGER':
                value = int(self.current_token[1])
            node = Node(value)
            self.next_token()
            return node
        elif self.current_token and self.current_token[0] == 'LPAREN':
            self.next_token()
            node = self.plus_minus()
            if self.current_token and self.current_token[0] == 'RPAREN':
                self.next_token()
                return node
            else:
                raise SyntaxError("Expected ')'")
        else:
            raise SyntaxError("Expected number or '('")

def evaluate(node):
    if isinstance(node.value, (float, int)):
        return node.value
    elif node.value == 'PLUS':
        return evaluate(node.left) + evaluate(node.right)
    elif node.value == 'MINUS':
        return evaluate(node.left) - evaluate(node.right)
    elif node.value == 'MULT':
        return evaluate(node.left) * evaluate(node.right)
    elif node.value == 'DIV':
        return evaluate(node.left) / evaluate(node.right)

data = "3 + 2 * (4 + 5)"
lexer = Lexer(data)
tokens = lexer.tokenize()
parser = Parser(tokens)
graph = parser.parse()
result = evaluate(graph)
print(f"Parser returns: {result}")
