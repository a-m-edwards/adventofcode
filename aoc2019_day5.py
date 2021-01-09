#Day 5 Part 1 and Part 2
path = 'aoc2019_day5.txt'
prog = list()
with open(path) as f:
    for l in f:
        prog = prog + [int(n) for n in l.rstrip().split(',')]
prog_copy = prog.copy()

def process_opcode(position, inpt):
    inst = str(prog[position]).zfill(5)
    opcode = int(inst[3:])
    param1_mode = int(inst[2])
    param2_mode = int(inst[1])
    param3_mode = int(inst[0])
    stop = 0
    new_pos = None
    outpt = None
    
    def get_value(param, mode):
        if mode == 0:
            val_pos = prog[position+param]
            val = prog[val_pos]
        if mode == 1:
            val = prog[position+param]
        return val
    
    if opcode == 1:
        val1 = get_value(1, param1_mode)
        val2 = get_value(2, param2_mode)
        output_pos = prog[position+3]
        prog[output_pos] = val1 + val2
        new_pos = position+4
        print('Opcode 1 '+str(inst)+','+str(prog[position+1])+','+str(prog[position+2])+','+str(prog[position+3])+', '+str(val1)+' + '+str(val2)+' = '+str(val1 + val2)+', saved at position '+str(output_pos))
        
    elif opcode == 2:
        val1 = get_value(1, param1_mode)
        val2 = get_value(2, param2_mode)
        output_pos = prog[position+3]
        prog[output_pos] = val1 * val2
        new_pos = position+4
        print('Opcode 2 '+str(inst)+','+str(prog[position+1])+','+str(prog[position+2])+','+str(prog[position+3])+', '+str(val1)+' * '+str(val2)+' = '+str(val1 * val2)+', saved at position '+str(output_pos))
        
    elif opcode == 3:
        output_pos = prog[position+1]
        prog[output_pos] = inpt
        new_pos = position+2
        print('Opcode 3 '+str(inst)+','+str(prog[position+1])+', input '+str(inpt)+' saved at position '+str(output_pos))
        
    elif opcode == 4:
        outpt = get_value(1, param1_mode)
        new_pos = position+2
        print('Opcode 4 '+str(inst)+','+str(prog[position+1])+', output = '+str(outpt))
    
    elif opcode == 5:
        val1 = get_value(1, param1_mode)
        val2 = get_value(2, param2_mode)
        if val1 != 0: new_pos = val2
        else: new_pos = position+3
        print('Opcode 5 '+str(inst)+','+str(prog[position+1])+','+str(prog[position+2])+', val1 = '+str(val1)+', jumping to position '+str(new_pos))
            
    elif opcode == 6:
        val1 = get_value(1, param1_mode)
        val2 = get_value(2, param2_mode)
        if val1 == 0: new_pos = val2
        else: new_pos = position+3
        print('Opcode 6 '+str(inst)+','+str(prog[position+1])+','+str(prog[position+2])+', val1 = '+str(val1)+', jumping to position '+str(new_pos))
        
    elif opcode == 7:
        val1 = get_value(1, param1_mode)
        val2 = get_value(2, param2_mode)
        output_pos = prog[position+3]
        if val1 < val2: 
            prog[output_pos] = 1
            print('Opcode 7 '+str(inst)+','+str(prog[position+1])+','+str(prog[position+2])+','+str(prog[position+3])+', 1 saved at position '+str(output_pos))
        else: 
            prog[output_pos] = 0
            print('Opcode 7 '+str(inst)+','+str(prog[position+1])+','+str(prog[position+2])+','+str(prog[position+3])+', 0 saved at position '+str(output_pos))
        new_pos = position+4

    elif opcode == 8:
        val1 = get_value(1, param1_mode)
        val2 = get_value(2, param2_mode)
        output_pos = prog[position+3]
        if val1 == val2: 
            prog[output_pos] = 1
            print('Opcode 8 '+str(inst)+','+str(prog[position+1])+','+str(prog[position+2])+','+str(prog[position+3])+', 1 saved at position '+str(output_pos))
        else: 
            prog[output_pos] = 0
            print('Opcode 8 '+str(inst)+','+str(prog[position+1])+','+str(prog[position+2])+','+str(prog[position+3])+', 0 saved at position '+str(output_pos))
        new_pos = position+4
    
    elif opcode == 99:
        stop = 1
        print('Opcode 99 '+str(inst))
    
    return stop, new_pos

#Part 1
sysid = 1
pos = 0
while True:
    print('Part 1 processing instruction at position '+str(pos))
    stop, pos = process_opcode(pos, sysid)
    if stop == 1: break

#Part 2
sysid = 5
pos = 0
prog = prog_copy.copy()
while True:
    print('Part 2 processing instruction at position '+str(pos)+' = '+str(prog[pos]))
    stop, pos = process_opcode(pos, sysid)
    if stop == 1: break