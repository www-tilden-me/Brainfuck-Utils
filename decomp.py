# @desc: reads a brainfuck file and translates it back to psuedocode
# @assumes: valid brainfuck code -- executes without overflow, out of bounds, or other
# @assumes: no user input -- no ","

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
        return str(value)

#try more of a simulator
memory = [0]*30_000
ptr = 0
while_stack = []

decompiled = """memory = [0]*30_000\n"""
changes = [0]*30_000

i = 0
while i < len(code):
    cmd = code[i]
    match cmd:
        case "+":
            changes[ptr] += 1
            
        case "-":
            changes[ptr] -= 1
            
        case ">":
            ptr += 1
            
        case "<":
            ptr -= 1
            
        case "[":
            while_stack += [i]
            
        case "]":
            last = while_stack.pop()
            if (memory[ptr] + changes[ptr] != 0):
                i = last
                continue

        case ",": # assume no inputs for now
            pass

        case ".":
            for j in range(len(changes)):
                memory[j] += changes[j]

                if (changes[j] != 0):
                    decompiled = add_command(decompiled, f"memory[{j}] = {check_printable(memory[j])}", 0)
                    changes[j] = 0
            
            decompiled = add_command(decompiled, f"print({check_printable(memory[ptr])})", 0)
            
    i+=1

print(decompiled)