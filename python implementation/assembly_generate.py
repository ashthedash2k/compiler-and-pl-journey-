from parser import * 
from lexer import *

class AssemblyGenerator:
    def __init__(self):
        self.registers = ['rax', 'rbx', 'rcx', 'rdx', 'rsi', 'rdi', 'r8', 'r9']  
        self.used_registers = []  
        self.stack = []
        self.stack_offset = 0

    def get_register(self):
        if self.registers:
            reg = self.registers.pop(0)
            self.used_registers.append(reg)
            return reg
        else:
            return self.spill_to_stack()

    def release_register(self, reg):
        if reg in self.used_registers:
            self.used_registers.remove(reg)
            self.registers.append(reg)

    def spill_to_stack(self):
        if self.used_registers:
            spill_reg = self.used_registers[-1]
            self.stack.append(spill_reg)
            self.used_registers.pop()
            self.registers.append(spill_reg)
            return spill_reg
        else:
            raise Exception("No registers to spill")
        
    
    def push_to_stack(self, reg):
        self.stack.append(reg)
        return f"push {reg}"

    def pop_from_stack(self, reg):
        self.stack.remove(reg)
        return f"pop {reg}"

    def increase_rsp(self, value):
        return f"add rsp, {value}"

    def decrease_rsp(self, value):
        return f"sub rsp, {value}"
    
    def print_stack(self):
        if not self.stack:
            print("Stack is empty.")
            return

        print("Stack contents (top to bottom):")
        for item in reversed(self.stack):
            print(item)

    def assembly(self, node):
        asm = []
        if node is None:
            return asm

        if isinstance(node.value, int):
            reg = self.get_register()
            asm.append(f"mov {reg}, {node.value}")
        elif node.value in ['PLUS', 'MINUS', 'MULT', 'DIV']:
            if node.left:
                left_asm = self.assembly(node.left)
                asm.extend(left_asm)
                left_reg = self.used_registers[-1]
            else:
                raise Exception("Missing left operand")

            if node.right:
                right_asm = self.assembly(node.right)
                asm.extend(right_asm)
                right_reg = self.used_registers[-1]
            else:
                raise Exception("Missing right operand")

            asm.append(self.push_to_stack(right_reg))
            self.release_register(right_reg)

            if node.value == 'PLUS':
                asm.append(f"add {left_reg}, [rsp]")  

            asm.append(self.pop_from_stack(right_reg)) 

        return asm

data = "(5 + 2) + (6 + 7)"
lexer = Lexer(data)
tokens = lexer.tokenize()
parser = Parser(tokens)

try:
    graph = parser.parse()
    graph.print_tree()
    result = parser.evaluate(graph)
    print(f"Parser returns: {result}")
    print(f'Symbol table values: {parser.symbol_table}')

    generator = AssemblyGenerator()  
    assembly_code = generator.assembly(graph) 
    generator.print_stack()
    print("\n".join(assembly_code))
except SyntaxError as e:
    print(f"Syntax error in parsing: {e}")

