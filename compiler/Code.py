import os
class Code:
    instructions = []

    def append(instruction):
        Code.instructions.append(instruction)

    def dump(filename):
        
        base_name = os.path.splitext(filename)[0]
        asm_filename = base_name + ".asm"

        with open(asm_filename, 'w') as f:
            
            f.write("section .data\n")
            f.write('format_out: db "%d", 10, 0\n')
            f.write('format_in: db "%d", 0\n')
            f.write('scan_int: dd 0\n\n')

            f.write("section .text\n")
            f.write("extern printf\n")
            f.write("extern scanf\n")
            f.write("global _start\n\n")

            f.write("_start:\n")
            f.write("    push ebp\n")
            f.write("    mov ebp, esp\n\n")

            
            for instr in Code.instructions:
                f.write(f"    {instr}\n")

            
            f.write("\n    mov esp, ebp\n")
            f.write("    pop ebp\n")
            f.write("    mov eax, 1\n")
            f.write("    xor ebx, ebx\n")
            f.write("    int 0x80\n")
