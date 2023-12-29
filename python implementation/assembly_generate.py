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

    def assembly(self, node, target_reg=None):
        asm = []
        if node is None:
            return asm

        if isinstance(node.value, int):
            if target_reg is None:
                reg = self.get_register()
                asm.append(f"mov {reg}, {node.value}")
            else:
                asm.append(f"add {target_reg}, {node.value}")
        elif node.value in ['PLUS', 'MULT']:  # Commutative operations
            if target_reg is None:
                target_reg = self.get_register()

            if node.is_commutative and isinstance(node.right.value, int):
                node.left, node.right = node.right, node.left

            if node.left:
                left_asm = self.assembly(node.left, target_reg)
                asm.extend(left_asm)
            
            if node.right:
                right_asm = self.assembly(node.right, target_reg)
                asm.extend(right_asm)

            if target_reg not in self.used_registers:
                self.release_register(target_reg)

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

