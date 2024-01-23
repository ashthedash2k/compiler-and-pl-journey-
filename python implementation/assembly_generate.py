from parser import * 
from lexer import *

class AssemblyGenerator:
    def __init__(self):
        self.registers = ['rax', 'rbx', 'rcx', 'rdx', 'rsi', 'rdi', 'rsp', 'r8', 'r9']  
        #self.registers_32_bit = ['eax', 'ebx', 'ecx', 'edx', 'esi', 'edi', 'esp']
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

    def assembly(self, node, target_reg='rax', operation=None):
        asm = []
        if node is None:
            return asm

        if isinstance(node.value, int):
            # First integer initializes the target register
            if operation is None:
                asm.append(f"mov {target_reg}, {node.value}")
            else:
                if operation == 'PLUS':
                    asm.append(f"add {target_reg}, {node.value}")
                elif operation == 'MULT':
                    asm.append(f"mul {target_reg}, {node.value}")
        else:
            # Update the operation if current node is an operation
            if node.value in ['PLUS', 'MULT']:
                operation = node.value

            # Process left and right operands
            if node.left:
                asm += self.assembly(node.left, target_reg, operation)
            if node.right:
                asm += self.assembly(node.right, target_reg, operation)

        return asm

data = "(5 * 2) + (1 * 7)"
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

