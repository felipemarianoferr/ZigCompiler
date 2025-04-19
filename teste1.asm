section .data
format_out: db "%d", 10, 0
format_in: db "%d", 0
scan_int: dd 0

section .text
extern printf
extern scanf
global _start

_start:
    push ebp
    mov ebp, esp

    sub esp, 4
    sub esp, 4
    mov eax,1
    neg eax
    push eax
    mov eax,3
    pop ecx
    add eax, ecx
    mov [ebp-4], eax
    mov eax, [ebp-4]
    mov [ebp-8], eax
    mov eax,5
    push eax
    mov eax, [ebp-4]
    pop ecx
    cmp ecx, eax
    mov eax, 0
    mov ebx, 1
    cmovl eax, ecx
    push eax
    mov eax,1
    push eax
    mov eax, [ebp-4]
    pop ecx
    cmp ecx, eax
    mov eax, 0
    mov ebx, 1
    cmovg eax, ecx
    pop ecx
    test eax, eax
    jne true_or_18
    test ecx, ecx
    jne true_or_18
    mov eax, 0
    jmp end_or_18
    true_or_18:
    mov eax, 1
    end_or_18:
    cmp eax, 0
    je else_22
    mov eax,1
    push eax
    mov eax,5
    pop ecx
    sub eax, ecx
    mov [ebp-4], eax
    jmp endif_22
    else_22:
    endif_22:
    mov eax,3
    push eax
    mov eax, [ebp-8]
    pop ecx
    cmp eax, ecx
    mov eax, 0
    mov ebx, 1
    cmove eax, ecx
    push eax
    mov eax,3
    push eax
    mov eax, [ebp-4]
    pop ecx
    cmp eax, ecx
    mov eax, 0
    mov ebx, 1
    cmove eax, ecx
    pop ecx
    test eax, eax
    je false_and_32
    test ecx, ecx
    je false_and_32
    mov eax, 1
    jmp end_and_32
    false_and_32:
    mov eax, 0
    end_and_32:
    cmp eax, 0
    je else_36
    jmp endif_36
    else_36:
    mov eax,3
    mov [ebp-4], eax
    endif_36:
    mov eax,3
    mov [ebp-4], eax
    loop_49:
    mov eax,5
    push eax
    mov eax, [ebp-4]
    pop ecx
    cmp ecx, eax
    mov eax, 0
    mov ebx, 1
    cmovl eax, ecx
    cmp eax, 0
    je exit_49
    mov eax,1
    push eax
    mov eax, [ebp-4]
    pop ecx
    sub eax, ecx
    mov [ebp-8], eax
    mov eax,1
    push eax
    mov eax, [ebp-4]
    pop ecx
    add eax, ecx
    mov [ebp-4], eax
    jmp loop_49
    exit_49:
    mov eax, [ebp-4]
    push eax
    push format_out
    call printf
    add esp, 8

    mov esp, ebp
    pop ebp
    mov eax, 1
    xor ebx, ebx
    int 0x80
