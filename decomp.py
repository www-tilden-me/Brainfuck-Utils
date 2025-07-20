# @desc: reads a brainfuck file and translates it back to psuedocode
# @assumes: valid brainfuck code -- executes without overflow, out of bounds, or other
# @assumes: no user input -- no ","

import sys
import re

filename = sys.argv[1]
with open(filename, "r") as file:
    code = file.read()

def add_command(program, cmd_str, indentation):
    program += "\t"*indentation + cmd_str + "\n"
    return program

#try more of a simulator
result = ""

memory = [0]*30_000
ptr = 0
while_stack = []
i = 0
while i < len(code):
    cmd = code[i]
    match cmd:
        case "+":
            memory[ptr] += 1
            
        case "-":
            memory[ptr] -= 1
            
        case ">":
            ptr += 1
            
        case "<":
            ptr -= 1
            
        case "[":
            while_stack += [i]
            
        case "]":
            last = while_stack.pop()
            if (memory[ptr] != 0):
                i = last
                continue

        case ",": # assume no inputs for now
            pass

        case ".":
            result += chr(memory[ptr])
            
    i+=1

print(result)