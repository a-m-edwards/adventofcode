#Day 2 Part 1 and Part 2
path = 'aoc2019_day2.txt'
prog = list()
with open(path) as f:
    for l in f:
        prog = prog + [int(n) for n in l.rstrip().split(',')]
prog_copy = prog.copy()
        
def process_opcode(position):
    opcode = prog[position]
    input_pos1 = prog[position+1]
    input_pos2 = prog[position+2]
    output_pos = prog[position+3]
    stop = 0
    if input_pos1 > len(prog)-1 or input_pos2 > len(prog)-1 or output_pos > len(prog)-1:
        stop = 1
    elif opcode == 1:
        prog[output_pos] = prog[input_pos1] + prog[input_pos2]
    elif opcode == 2:
        prog[output_pos] = prog[input_pos1] * prog[input_pos2]
    elif opcode == 99:
        stop = 1
    return stop

#before running the program, replace position 1 with the value 12 and replace position 2 with the value 2
prog[1] = 12
prog[2] = 2
for i in range(0,len(prog),4):
    x = process_opcode(i)
    if x == 1: break

print('Part 1 position 0 value = '+str(prog[0]))

for noun in range(0,99+1):
    for verb in range(0,99+1):
        prog = prog_copy.copy()
        prog[1] = noun
        prog[2] = verb
        for i in range(0,len(prog),4):
            x = process_opcode(i)
            if x == 1: break
        if prog[0] == 19690720: break
    if prog[0] == 19690720:
        print('Part 2 noun = '+str(noun)+', verb = '+str(verb)+', 100 * noun + verb = '+str(100*noun+verb))
        break