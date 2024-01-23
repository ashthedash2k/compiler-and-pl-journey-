from parser import * 
from lexer import *

class AssemblyGenerator:
    def __init__(self):
        self.registers = ['eax', 'ebx', 'ecx', 'edx', 'esi', 'edi', 'esp', 'ebp', 'r8d', 'r9d']  
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

    def assembly(self, node, target_reg=None):
        asm = []
        if node is None:
            return asm, None

        if isinstance(node.value, int):
            reg = self.get_register() if target_reg is None else target_reg
            asm.append(f"mov {reg}, {node.value}")
            return asm, reg

        if node.value in ['PLUS', 'MULT']:
            left_asm, left_reg = self.assembly(node.left)
            right_asm, right_reg = self.assembly(node.right)

            asm += left_asm
            asm.append(f"push {left_reg}")  
            asm += right_asm

            asm.append(f"pop {left_reg}")   
            if node.value == 'PLUS':
                asm.append(f"add {left_reg}, {right_reg}")
            elif node.value == 'MULT':
                asm.append(f"imul {left_reg}, {right_reg}")

            self.release_register(right_reg)
            return asm, left_reg

        return asm, None

def flatten(lst):
    flat_list = []
    for item in lst:
        if isinstance(item, list):
            flat_list.extend(flatten(item)) 
        else:
            flat_list.append(item) 
    return flat_list



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
    assembly_code, _ = generator.assembly(graph)
    assembly_code = flatten(assembly_code) 
    print(assembly_code)
    print("\n".join(assembly_code))
except SyntaxError as e:
    print(f"Syntax error in parsing: {e}")
