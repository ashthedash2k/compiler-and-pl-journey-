'''
Run everything in here. Read in a file of python code. 
'''

def main():
    file_path = '/Users/ashthedash/compiler_journey/python implementation/code.txt'
    with open(file_path, 'r') as file:
        return file.read()


if __name__ == '__main__':
    main()