#Day 9 Part 1 and Part 2
path = 'aoc2019_day9.txt'
day9 = dict()
index = 0
with open(path) as f:
    for l in f:
        for n in l.rstrip().split(','):
            day9[index] = int(n)
            index += 1
    
def process_opcode(position, input1, input2, input_count, prog, rel_base):
    inst = str(prog[position]).zfill(5)
    opcode = int(inst[3:])
    param1_mode = int(inst[2])
    param2_mode = int(inst[1])
    param3_mode = int(inst[0])
    stop = 0
    new_pos = None
    outpt = None
    
    def get_value(param, mode, rel_base):
        if mode == 0:
            val_pos = prog.get(position+param, 0)
            val = prog.get(val_pos, 0)
        elif mode == 1:
            val = prog.get(position+param, 0)
        elif mode == 2:
            val_pos = rel_base + prog.get(position+param, 0)
            val = prog.get(val_pos, 0)
        #print('Value '+str(param)+', mode '+str(mode)+' = '+str(val))
        return val
    
    def find_output_pos(param, mode, rel_base):
        if mode == 0:
            out_pos = prog.get(position+param, 0)
        elif mode == 2:
            out_pos = rel_base + prog.get(position+param, 0)
        #print('Value '+str(param)+', mode '+str(mode)+', output position = '+str(out_pos))
        return out_pos
    
    if opcode == 1:
        val1 = get_value(1, param1_mode, rel_base)
        val2 = get_value(2, param2_mode, rel_base)
        output_pos = find_output_pos(3, param3_mode, rel_base)
        prog[output_pos] = val1 + val2
        new_pos = position+4
        #print('Opcode 1 '+str(inst)+','+str(prog[position+1])+','+str(prog[position+2])+','+str(prog[position+3])+', '+str(val1)+' + '+str(val2)+' = '+str(val1 + val2)+', saved at position '+str(output_pos))
        
    elif opcode == 2:
        val1 = get_value(1, param1_mode, rel_base)
        val2 = get_value(2, param2_mode, rel_base)
        output_pos = find_output_pos(3, param3_mode, rel_base)
        prog[output_pos] = val1 * val2
        new_pos = position+4
        #print('Opcode 2 '+str(inst)+','+str(prog[position+1])+','+str(prog[position+2])+','+str(prog[position+3])+', '+str(val1)+' * '+str(val2)+' = '+str(val1 * val2)+', saved at position '+str(output_pos))
        
    elif opcode == 3:
        input_count += 1
        if input_count == 1: inpt = input1
        elif input_count > 1: inpt = input2
        
        output_pos = find_output_pos(1, param1_mode, rel_base)
        prog[output_pos] = inpt
        new_pos = position+2
        #print('Opcode 3 '+str(inst)+','+str(prog[position+1])+', input '+str(inpt)+' saved at position '+str(output_pos))
        
    elif opcode == 4:
        outpt = get_value(1, param1_mode, rel_base)
        new_pos = position+2
        #print('Opcode 4 '+str(inst)+','+str(prog[position+1])+', output = '+str(outpt))
    
    elif opcode == 5:
        val1 = get_value(1, param1_mode, rel_base)
        val2 = get_value(2, param2_mode, rel_base)
        if val1 != 0: new_pos = val2
        else: new_pos = position+3
        #print('Opcode 5 '+str(inst)+','+str(prog[position+1])+','+str(prog[position+2])+', val1 = '+str(val1)+', jumping to position '+str(new_pos))
            
    elif opcode == 6:
        val1 = get_value(1, param1_mode, rel_base)
        val2 = get_value(2, param2_mode, rel_base)
        if val1 == 0: new_pos = val2
        else: new_pos = position+3
        #print('Opcode 6 '+str(inst)+','+str(prog[position+1])+','+str(prog[position+2])+', val1 = '+str(val1)+', jumping to position '+str(new_pos))
        
    elif opcode == 7:
        val1 = get_value(1, param1_mode, rel_base)
        val2 = get_value(2, param2_mode, rel_base)
        output_pos = find_output_pos(3, param3_mode, rel_base)
        if val1 < val2: 
            prog[output_pos] = 1
            #print('Opcode 7 '+str(inst)+','+str(prog[position+1])+','+str(prog[position+2])+','+str(prog[position+3])+', 1 saved at position '+str(output_pos))
        else: 
            prog[output_pos] = 0
            #print('Opcode 7 '+str(inst)+','+str(prog[position+1])+','+str(prog[position+2])+','+str(prog[position+3])+', 0 saved at position '+str(output_pos))
        new_pos = position+4
        
    elif opcode == 8:
        val1 = get_value(1, param1_mode, rel_base)
        val2 = get_value(2, param2_mode, rel_base)
        output_pos = find_output_pos(3, param3_mode, rel_base)
        if val1 == val2: 
            prog[output_pos] = 1
            #print('Opcode 8 '+str(inst)+','+str(prog[position+1])+','+str(prog[position+2])+','+str(prog[position+3])+', 1 saved at position '+str(output_pos))
        else: 
            prog[output_pos] = 0
            #print('Opcode 8 '+str(inst)+','+str(prog[position+1])+','+str(prog[position+2])+','+str(prog[position+3])+', 0 saved at position '+str(output_pos))
        new_pos = position+4
    
    elif opcode == 9:
        val1 = get_value(1, param1_mode, rel_base)
        rel_base = rel_base + val1
        new_pos = position+2
        #print('Opcode 9 '+str(inst)+','+str(prog[position+1])+', relative base = '+str(rel_base))
    
    elif opcode == 99:
        stop = 1
        #print('Opcode 99 '+str(inst))
    
    return stop, new_pos, input_count, outpt, rel_base

def run_boost(inpt, prog):
    prog_copy = prog.copy()
    pos = 0
    input_count = 0
    rel_base = 0
    boost_output = list()
    while True:
        #print('Processing instruction at position '+str(pos))
        stop, pos, input_count, outpt, rel_base = process_opcode(pos, inpt, 0, input_count, prog_copy, rel_base)
        if outpt != None: boost_output.append(outpt)
        if stop == 1: break
    return boost_output

#Part 1 test input
test_txt = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
test = dict()
index = 0
for n in test_txt.split(','):
    test[index] = int(n)
    index += 1

part1 = run_boost(1,day9)
print('Part 1 BOOST keycode = '+str(part1[0]))

part2 = run_boost(2,day9)
print('Part 2 coordinates = '+str(part2[0]))