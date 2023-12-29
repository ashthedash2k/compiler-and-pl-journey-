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
            else: 
                left_asm = []
            
            asm.extend(left_asm)
            if left_asm: 
                left_reg = self.used_registers[-1]
            else: 
                left_reg = None
            
            if node.right:
                right_asm = self.assembly(node.right)
            else: 
                right_asm = []

            asm.extend(right_asm)

            if right_asm: 
                right_reg = self.used_registers[-1]
            else: 
                right_reg = None
            
            if left_reg and right_reg:
                if node.value == 'PLUS':
                    asm.append(f"add {left_reg}, {right_reg}")
                    self.release_register(right_reg)
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
    print("\n".join(assembly_code))
except SyntaxError as e:
    print(f"Syntax error in parsing: {e}")

