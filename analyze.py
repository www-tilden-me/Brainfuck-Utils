# @desc: analyzes a bf file and attempt to calculate program cost

import sys
import random
import tabulate

###CONSTANTS
size_cost = 0 #Tracks size of the file to accomplish task -- # cmds
exec_cost = 0 #Tracks cost of executing commands (averaged across inputs)
memory_cost = 0 #Tracks amount of memory used (averaged across inputs)

ptr_move_cost = 1
mem_update_cost = 2
while_start_cost = 10
check_cost = 50
write_cost = 1000
read_cost = 2000
###

def analyze(code, putchar, getchar):
	exec_cost = 0
	memory_cost = 0
	accessed_memory = {0}

	memory = [0]*30_000
	while_stack = []
	ptr = 0

	i = 0
	while i < len(code):
		cmd = code[i]
		match cmd:
			case "+":
				exec_cost += mem_update_cost
				accessed_memory.add(ptr)
				memory[ptr] = (memory[ptr] + 1) % 255

			case "-":
				exec_cost += mem_update_cost
				accessed_memory.add(ptr)
				memory[ptr] = (memory[ptr] - 1) % 255

			case ">":
				exec_cost += ptr_move_cost
				ptr += 1

			case "<":
				exec_cost += ptr_move_cost
				ptr -= 1

			case "[":
				exec_cost += while_start_cost
				while_stack += [i]

			case "]":
				exec_cost += check_cost
				accessed_memory.add(ptr)
				last = while_stack.pop()
				if (memory[ptr] != 0):
					i = last
					continue

			case ".":
				exec_cost += write_cost
				accessed_memory.add(ptr)
				putchar(memory[ptr])

			case ",":
				exec_cost += read_cost
				accessed_memory.add(ptr)
				memory[ptr] = getchar()

		i+= 1
	memory_cost = len(list(accessed_memory))
	return (exec_cost, memory_cost)

file_name = sys.argv[1]

with open(file_name, "r") as file:
	code = file.read()

N = 1000
size_cost = len(code)

def simulated_putchar(*args, **kwargs):
	pass

def simulated_getchar(*args, **kwargs):
	return random.randint(0,255)

exec_cost = 0
memory_cost = 0
for _ in range(N):
	ec, mc = analyze(code, simulated_putchar, simulated_getchar)
	exec_cost += ec
	memory_cost += mc 

COSTS = f"""
COST OF \"{file_name}\" ({N} trails):
"""
data = [
	["Size", size_cost],
	["Memory", memory_cost//N],
	["Execution", exec_cost//N],
	["Avg. Total", (size_cost+memory_cost+exec_cost)//(3*N)]
]
COSTS += tabulate.tabulate(data, headers=["Name", "Cost"], tablefmt="pretty")
print(COSTS.strip())

