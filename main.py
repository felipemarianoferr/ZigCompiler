from compiler.Parser import *
import sys

if __name__ == "__main__":

    # source = sys.argv[1]

    # try:
    #     with open(source, "r") as arquivo:
    #         code = arquivo.read()
    # except FileNotFoundError:
    #     code = source
    code = """
    {
        a = 3;
        b = 0;

        while (a > 0) {
            b = b + 2;
            a = a - 1;
        }

        if (b == 6 && !(a > 0)) {
            print(b);
        } else {
            print(a);
        }
    }
    """
    Parser.run(code)