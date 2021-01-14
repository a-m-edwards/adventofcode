#Day 7 Part 1
from itertools import permutations
perms = {index : None for index in list(permutations([0,1,2,3,4]))}

path = 'aoc2019_day7.txt'
day7 = list()
with open(path) as f:
    for l in f:
        day7 = day7 + [int(n) for n in l.rstrip().split(',')]

def process_opcode(position, input1, input2, input_count, prog):
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
        #print('Opcode 1 '+str(inst)+','+str(prog[position+1])+','+str(prog[position+2])+','+str(prog[position+3])+', '+str(val1)+' + '+str(val2)+' = '+str(val1 + val2)+', saved at position '+str(output_pos))
        
    elif opcode == 2:
        val1 = get_value(1, param1_mode)
        val2 = get_value(2, param2_mode)
        output_pos = prog[position+3]
        prog[output_pos] = val1 * val2
        new_pos = position+4
        #print('Opcode 2 '+str(inst)+','+str(prog[position+1])+','+str(prog[position+2])+','+str(prog[position+3])+', '+str(val1)+' * '+str(val2)+' = '+str(val1 * val2)+', saved at position '+str(output_pos))
        
    elif opcode == 3:
        input_count += 1
        if input_count == 1: inpt = input1
        elif input_count > 1: inpt = input2
            
        output_pos = prog[position+1]
        prog[output_pos] = inpt
        new_pos = position+2
        #print('Opcode 3 '+str(inst)+','+str(prog[position+1])+', input '+str(inpt)+' saved at position '+str(output_pos))
        
    elif opcode == 4:
        outpt = get_value(1, param1_mode)
        new_pos = position+2
        #print('Opcode 4 '+str(inst)+','+str(prog[position+1])+', output = '+str(outpt))
    
    elif opcode == 5:
        val1 = get_value(1, param1_mode)
        val2 = get_value(2, param2_mode)
        if val1 != 0: new_pos = val2
        else: new_pos = position+3
        #print('Opcode 5 '+str(inst)+','+str(prog[position+1])+','+str(prog[position+2])+', val1 = '+str(val1)+', jumping to position '+str(new_pos))
            
    elif opcode == 6:
        val1 = get_value(1, param1_mode)
        val2 = get_value(2, param2_mode)
        if val1 == 0: new_pos = val2
        else: new_pos = position+3
        #print('Opcode 6 '+str(inst)+','+str(prog[position+1])+','+str(prog[position+2])+', val1 = '+str(val1)+', jumping to position '+str(new_pos))
        
    elif opcode == 7:
        val1 = get_value(1, param1_mode)
        val2 = get_value(2, param2_mode)
        output_pos = prog[position+3]
        if val1 < val2: 
            prog[output_pos] = 1
            #print('Opcode 7 '+str(inst)+','+str(prog[position+1])+','+str(prog[position+2])+','+str(prog[position+3])+', 1 saved at position '+str(output_pos))
        else: 
            prog[output_pos] = 0
            #print('Opcode 7 '+str(inst)+','+str(prog[position+1])+','+str(prog[position+2])+','+str(prog[position+3])+', 0 saved at position '+str(output_pos))
        new_pos = position+4

    elif opcode == 8:
        val1 = get_value(1, param1_mode)
        val2 = get_value(2, param2_mode)
        output_pos = prog[position+3]
        if val1 == val2: 
            prog[output_pos] = 1
            #print('Opcode 8 '+str(inst)+','+str(prog[position+1])+','+str(prog[position+2])+','+str(prog[position+3])+', 1 saved at position '+str(output_pos))
        else: 
            prog[output_pos] = 0
            #print('Opcode 8 '+str(inst)+','+str(prog[position+1])+','+str(prog[position+2])+','+str(prog[position+3])+', 0 saved at position '+str(output_pos))
        new_pos = position+4
    
    elif opcode == 99:
        stop = 1
        #print('Opcode 99 '+str(inst))
    
    return stop, new_pos, input_count, outpt

def run_amp(phase_setting, signal, prog):
    prog_copy = prog.copy()
    pos = 0
    input_count = 0
    amp_output = None
    while True:
        #print('Processing instruction at position '+str(pos))
        stop, pos, input_count, outpt = process_opcode(pos, phase_setting, signal, input_count, prog_copy)
        if outpt != None: amp_output = outpt
        if stop == 1: break
    return amp_output

#Part 1 test input
test_txt = '3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0'
test = [int(n) for n in test_txt.split(',')]
phase_txt = '0,1,2,3,4'
phases_test = [int(n) for n in phase_txt.split(',')]

for perm in perms:
    amp_output = 0
    for phase in perm:
        amp_output = run_amp(phase,amp_output,day7)
    perms[perm] = amp_output

max_output = max(perms.values())
for perm in perms:
    if perms[perm] == max_output: 
        print('Part 1 max thruster signal = '+str(max_output)+' from sequence '+str(perm))

#Part 2 test input
p2test_txt = '3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'
p2test = [int(n) for n in p2test_txt.split(',')]
p2phase_txt = '9,8,7,6,5'
p2phases_test = [int(n) for n in p2phase_txt.split(',')]

part2perms = {index : None for index in list(permutations([5,6,7,8,9]))}
amps = {amp : dict() for amp in [1,2,3,4,5]}
for amp in amps:
    amps[amp]['pos'] = 0
    amps[amp]['input_count'] = 0
    amps[amp]['phase_setting'] = None

def run_amp_p2(amp, signal, prog):
    prog_copy = amps[amp][prog]
    pos = amps[amp]['pos']
    input_count = amps[amp]['input_count']
    phase_setting = amps[amp]['phase_setting']
    amp_output = None
    while True:
        #print('Processing instruction at position '+str(pos))
        stop, pos, input_count, outpt = process_opcode(pos, phase_setting, signal, input_count, prog_copy)
        if outpt != None: 
            amp_output = outpt
            amps[amp][prog] = prog_copy
            amps[amp]['pos'] = pos
            amps[amp]['input_count'] = input_count
            break
        if stop == 1:
            break
    return amp_output, stop

for perm in part2perms:
    prog = day7
    prog_str = 'day7'
    amps[1]['phase_setting'],amps[2]['phase_setting'],amps[3]['phase_setting'],amps[4]['phase_setting'],amps[5]['phase_setting'] = perm[0],perm[1],perm[2],perm[3],perm[4]
    amps[1][prog_str],amps[2][prog_str],amps[3][prog_str],amps[4][prog_str],amps[5][prog_str] = prog.copy(),prog.copy(),prog.copy(),prog.copy(),prog.copy()
    amps[1]['pos'],amps[2]['pos'],amps[3]['pos'],amps[4]['pos'],amps[5]['pos'] = 0,0,0,0,0
    amps[1]['input_count'],amps[2]['input_count'],amps[3]['input_count'],amps[4]['input_count'],amps[5]['input_count'] = 0,0,0,0,0
    amp_output = 0
    perm_output = None
    amp = 1
    while True:
        #print('Running amp '+str(amp)+' for seqeunce '+str(perm))
        amp_output, stop = run_amp_p2(amp, amp_output, prog_str)
        if stop == 1: break
        if amp_output != None:
            if amp == 5: perm_output = amp_output
            amp += 1
            if amp > 5: amp = 1
    part2perms[perm] = perm_output

max_output_p2 = max(part2perms.values())
for perm in part2perms:
    if part2perms[perm] == max_output_p2: 
        print('Part 2 max thruster signal = '+str(max_output_p2)+' from sequence '+str(perm))