# @desc: reads a brainfuck file and translates it back to psuedocode
# @assumes: valid brainfuck code -- executes without overflow, out of bounds, or other

import sys
import string

filename = sys.argv[1]
with open(filename, "r") as file:
    code = file.read()

def add_command(program, cmd_str, indentation):
    program += "\t"*indentation + cmd_str + "\n"
    return program

def check_printable(value):
    if chr(value) in string.printable:
        return repr(chr(value))
    else:
        return value

def this_while_has_read(code, start):
    total = 0
    
    code = code[start:]
    for i in range(len(code)):
        cmd = code[i]
        if (cmd == "["):
            total += 1
        if (cmd == "]"):
            total -= 1
        if (cmd == ','):
            return True

        if total == 0:
            return False

#try more of a simulator
memory = [0]*30_000
ptr = 0
while_stack = []

decompiled = """memory = [0]*30_000\n"""
changes = [0]*30_000
arith = 0
ptr_math = 0
indentation = 0
hasread = False

i = 0
while i < len(code): # TODO: Add check infection from reads/input
    cmd = code[i]
    match cmd:
        case "+":
            if (not hasread):
                changes[ptr] += 1
            else:
                if (ptr_math != 0):
                    decompiled = add_command(decompiled, f"ptr += {ptr_math}", indentation)
                    ptr_math = 0
                arith += 1
            
        case "-":
            if (not hasread):
                changes[ptr] -= 1
            else:
                if (ptr_math != 0):
                    decompiled = add_command(decompiled, f"ptr += {ptr_math}", indentation)
                    ptr_math = 0
                arith -= 1

        case ">":
            if (not hasread):
                ptr += 1
            else:
                if (arith != 0):
                    decompiled = add_command(decompiled, f"memory[ptr] += {arith}", indentation)
                    arith = 0
                ptr_math += 1
            
        case "<":
            if (not hasread):
                ptr -= 1
            else:
                if (arith != 0):
                    decompiled = add_command(decompiled, f"memory[ptr] += {arith}", indentation)
                    arith = 0
                ptr_math -= 1
            
        case "[":
            while_stack += [i]

            if (not hasread and this_while_has_read(code, i)):
                hasread = True
                decompiled = add_command(decompiled, f"ptr = {ptr}", indentation)
                for j in range(len(changes)):
                    memory[j] += changes[j]

                    if (changes[j] != 0):
                        decompiled = add_command(decompiled, f"memory[{j}] = {check_printable(memory[j])}", 0)
                        changes[j] = 0

            if hasread:
                if (arith):
                    decompiled = add_command(decompiled, f"memory[ptr] += {arith}", indentation)
                    arith = 0
                if (ptr_math != 0):
                    decompiled = add_command(decompiled, f"ptr += {ptr_math}", indentation)
                    ptr_math = 0
                
                decompiled = add_command(decompiled, f"\nwhile memory[ptr] != 0:", indentation)
            
            indentation += 1

        case "]":
            last = while_stack.pop()
            if (not hasread):
                if (memory[ptr] + changes[ptr] != 0):
                    i = last
                    indentation -= 1
                    continue
            
            if hasread:
                if (arith):
                    decompiled = add_command(decompiled, f"memory[ptr] += {arith}", indentation)
                    arith = 0
                if (ptr_math != 0):
                    decompiled = add_command(decompiled, f"ptr += {ptr_math}", indentation)
                    ptr_math = 0
                decompiled = add_command(decompiled, "", indentation)

            indentation -= 1

        case ",":
            if (hasread):
                if (arith):
                    decompiled = add_command(decompiled, f"memory[ptr] += {arith}", indentation)
                    arith = 0
                if (ptr_math != 0):
                    decompiled = add_command(decompiled, f"ptr += {ptr_math}", indentation)
                    ptr_math = 0

            else:
                hasread = True
                for j in range(len(changes)):
                    memory[j] += changes[j]

                    if (changes[j] != 0):
                        decompiled = add_command(decompiled, f"memory[{j}] = {check_printable(memory[j])}", 0)
                        changes[j] = 0
                
                decompiled = add_command(decompiled, f"ptr = {ptr}", indentation)
            decompiled = add_command(decompiled, "memory[ptr] = getchar()", indentation)

        case ".":
            if (not hasread):
                for j in range(len(changes)):
                    memory[j] += changes[j]

                    if (changes[j] != 0):
                        decompiled = add_command(decompiled, f"memory[{j}] = {check_printable(memory[j])}", 0)
                        changes[j] = 0
                
                decompiled = add_command(decompiled, f"print({check_printable(memory[ptr])})", 0)
            else:
                if (arith):
                    decompiled = add_command(decompiled, f"memory[ptr] += {arith}", indentation)
                    arith = 0
                if (ptr_math != 0):
                    decompiled = add_command(decompiled, f"ptr += {ptr_math}", indentation)
                    ptr_math = 0

                decompiled = add_command(decompiled, f"print(memory[ptr])", indentation)
    i+=1

print(decompiled)