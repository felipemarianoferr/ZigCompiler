from compiler.Parser import *
import sys

if __name__ == "__main__":

    source = sys.argv[1]

    try:
        with open(source, "r") as arquivo:
            code = arquivo.read()
    except FileNotFoundError:
        code = source

    # codigo_teste = """
    #     var A: i32 = 2;
    #     fn myprint(text: str) void {
    #     printf(text);
    #     }

    #     fn fac(x: i32) i32 {
    #     if (x == 1) {
    #         return 1;
    #     }
    #     return x * fac(x-1);
    #     }
    #     fn sum(x: i32, y: i32) i32 {
    #     return x + y;
    #     }

    #     fn tautology() bool {
    #     return true;
    #     }

    #     fn main() void {
    #     var x_1:i32;
    #     x_1 = reader();
    #     var x_2:i32 = fac(4);
    #     printf(A); printf(x_2);
    #     {
    #         var x_2:i32 = 7;
    #         x_1 = 9;
    #         A = 8;
    #         printf(x_2);
    #     }
    #     printf(A);
    #     printf(x_1);
        
    #     if ((x_1 > 1 && !!!(x_1 < 1)) || x_1 == 9) {
    #         x_1 = 2;
    #     }

    #     var x:i32 = 3; // <- testando sem unários empilhados

    #     var y_1:i32 = 3;
    #     y_1 = sum(y_1, x_1);
    #     var z__:i32;
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
    #         printf(x_1);
    #         x_1 = x_1 + 1;
    #     }

    #     ;;;
    #     printf(x_1);
    #     printf(x);
    #     printf(z__+1);
        
    #     var y:i32 = 2;
    #     var z:i32;
    #     z = (y - 1);
    #     printf(y+z);
    #     printf(y-z);
    #     printf(y*z);
    #     printf(y/y);
    #     printf(y == z);
    #     printf(y < z);
    #     printf(y > z);
        
    #     var a:str;
    #     var b:str;
        
    #     x_1 = 1;
    #     y = 1; 
    #     z = 2;
    #     a = "abc";
    #     b = "def";
    #     myprint(a++b);
    #     myprint(a);
    #     printf(a++x_1);
    #     printf(x_1++a);
    #     printf(a++(x_1==1));
    #     printf(a == a);
    #     printf(a < b);
    #     printf(a > b);
    #     }
    #     """


    Parser.run(code)