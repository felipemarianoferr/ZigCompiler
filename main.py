from compiler.Parser import *
import sys

if __name__ == "__main__":

    source = sys.argv[1]

    try:
        with open(source, "r") as arquivo:
            code = arquivo.read()
    except FileNotFoundError:
        code = source
    # code = """
    #     {
    #     x_1 = reader();

    #     print(x_1);

    #     if ((x_1 > 1 && !(x_1 < 1)) || x_1 == 3) {
    #         x_1 = 2;
    #     }

    #     x = 3+6/3   *  2 -+-  +  2*4/2 + 0/1 -((6+ ((4)))/(2)); // Teste // Teste 2
    #     y_1 = 3;
    #     y_1 = y_1 + x_1;
    #     z__ = x + y_1;

    #     if (x_1 == 2) {
    #         x_1 = 2;
    #     }

    #     if (x_1 == 3) {
    #         x_1 = 2;
    #     } else {
    #         x_1 = 3;
    #     }

    #     x_1 = 0;
    #     while (x_1 < 1 || x == 2) {
    #         print(x_1);
    #         x_1 = x_1 + 1;
    #     }

    #     ;;;

    #     // Saida final;
    #     print(x_1);
    #     print(x);
    #     print(z__ + 1);
    #     }
    #     """

    Parser.run(code)