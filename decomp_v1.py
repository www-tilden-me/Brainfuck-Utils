# @desc: reads a brainfuck file and translates it back to psuedocode
import sys
import re

filename = sys.argv[1]
with open(filename, "r") as file:
    code = file.read()

def add_command(program, cmd_str, indentation):
    program += "\t"*indentation + cmd_str + "\n"
    return program

indentation = 0
arithmetic = 0
ptr_math = 0
decompiled = """memory = [0]*30_000;\nptr = 0;\n"""
for cmd in code:
    match cmd:
        case "+":
            if (ptr_math != 0):
                decompiled = add_command(decompiled, f"ptr += {ptr_math};", indentation)
                ptr_math = 0

            arithmetic += 1
            
        case "-":
            if (ptr_math != 0):
                decompiled = add_command(decompiled, f"ptr += {ptr_math};", indentation)
                ptr_math = 0

            arithmetic -= 1
            
        case ">":
            if (arithmetic != 0):
                decompiled = add_command(decompiled, f"memory[ptr] += {arithmetic};", indentation)
                arithmetic = 0

            ptr_math += 1
            
        case "<":
            if (arithmetic != 0):
                decompiled = add_command(decompiled, f"memory[ptr] += {arithmetic};", indentation)
                arithmetic = 0

            ptr_math -= 1
            
        case "[":
            if (arithmetic != 0):
                decompiled = add_command(decompiled, "memory[ptr] += {arithmetic};", indentation)
                arithmetic = 0
            if (ptr_math != 0):
                decompiled = add_command(decompiled, f"ptr += {ptr_math};", indentation)
                ptr_math = 0

            decompiled = add_command(decompiled, "while (true){", indentation)
            indentation += 1
            
        case "]":
            if (arithmetic != 0):
                decompiled = add_command(decompiled, f"memory[ptr] += {arithmetic};", indentation)
                arithmetic = 0
            if (ptr_math != 0):
                decompiled = add_command(decompiled, f"ptr += {ptr_math};", indentation)
                ptr_math = 0

            decompiled = add_command(decompiled, "if (memory[ptr] == 0){ break }", indentation)
            indentation -= 1
            decompiled = add_command(decompiled, "}", indentation)

        case ",":
            if (arithmetic != 0):
                decompiled = add_command(decompiled, f"memory[ptr] += {arithmetic};", indentation)
                arithmetic = 0
            if (ptr_math != 0):
                decompiled = add_command(decompiled, f"ptr += {ptr_math};", indentation)
                ptr_math = 0

            decompiled = add_command(decompiled, "memory[ptr] = getchar();", indentation)

        case ".":
            if (arithmetic != 0):
                decompiled = add_command(decompiled, f"memory[ptr] += {arithmetic};", indentation)
                arithmetic = 0
            if (ptr_math != 0):
                decompiled = add_command(decompiled, f"ptr += {ptr_math};", indentation)
                ptr_math = 0

            decompiled = add_command(decompiled, "print(memory[ptr]);", indentation)

print(decompiled)