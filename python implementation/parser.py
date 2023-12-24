from lexer import Lexer
class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value  
        self.left = left   
        self.right = right  
    
    def print_tree(self, level=0, prefix=""):
        indent = "    " * level
        branch = "|-- " if level > 0 else ""
        print(indent + prefix + branch + str(self.value))
        if self.left:
            self.left.print_tree(level + 1, "L")
        if self.right:
            self.right.print_tree(level + 1, "R")

class Parser:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.current_token = None
        self.next_token()

    def next_token(self):
        self.current_token = next(self.tokens, None)

    def parse(self):
        return self.plus_minus()

    
    def compare(self, left_node):
        while self.current_token and self.current_token[0] in ['GREATER THAN', 'LESS THAN', 'GREATER THAN EQUAL', 'LESS THAN EQUAL']:
            op = self.current_token[0]
            self.next_token()
            right_node = self.mult_div()
            left_node = Node(op, left_node, right_node)
        return left_node

    def plus_minus(self):
        node = self.mult_div()
        while self.current_token:
            if self.current_token[0] in ['PLUS', 'MINUS']:
                op = self.current_token[0]
                self.next_token()
                node = Node(op, node, self.mult_div())
            elif self.current_token[0] in ['GREATER THAN', 'LESS THAN', 'GREATER THAN EQUAL', 'LESS THAN EQUAL']:
                return self.compare(node)
            else:
                break
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
    elif node.value == 'GREATER THAN':
        return evaluate(node.left) > evaluate(node.right)
    elif node.value == 'LESS THAN':
        return evaluate(node.left) < evaluate(node.right)
    elif node.value == 'GREATER THAN EQUAL':
        return evaluate(node.left) >= evaluate(node.right)
    elif node.value == 'LESS THAN EQUAL':
        return evaluate(node.left) <= evaluate(node.right)


data = " 1 + 2 * (3 * 9) "
lexer = Lexer(data)
tokens = lexer.tokenize()
parser = Parser(tokens)
graph = parser.parse()
graph.print_tree()
result = evaluate(graph)

print(f"Parser returns: {result}")
