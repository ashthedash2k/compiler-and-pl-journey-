'''
Run everything in here. Read in a file of python code. 
'''
from lexer import Lexer
from parser import Parser  

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def main():
    file_path = '/Users/ashthedash/compiler_journey/python implementation/code.txt'
    code = read_file(file_path)

if __name__ == "__main__":
    main()