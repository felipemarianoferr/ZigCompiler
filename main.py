from compiler.Parser import *
import sys

if __name__ == "__main__":

    source = sys.argv[1]

    try:
        with open(source, "r") as arquivo:
            code = arquivo.read()
    except FileNotFoundError:
        code = source

    Parser.run(code)