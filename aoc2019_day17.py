#Day 17
path = 'aoc2019_day17.txt'
day17 = dict()
index = 0
with open(path) as f:
    for l in f:
        for n in l.rstrip().split(','):
            day17[index] = int(n)
            index += 1
    
def process_opcode(prog, position, inpt, rel_base):
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
    
    return stop, new_pos, outpt, rel_base

def run_part1(prog,panels):
    pos = 0
    rel_base = 0
    stop = 0
    inpt = None
    view = ''
    x = 0
    y = 0
   
    while True:
        stop, pos, outpt, rel_base = process_opcode(prog, pos, inpt, rel_base)
        
        if outpt != None:
            view = view + chr(outpt)
        if stop == 1: 
            print(view)
            break
    
    for c in view:
        panels[(x,y)] = dict()
        panels[(x,y)]['char'] = c
        panels[(x,y)]['type'] = None
        panels[(x,y)]['visited'] = 0
        x += 1
        if c == '\n': 
            y += 1
            x = 0
        
    return panels

day17_copy = day17.copy()
panels = dict()
panels = run_part1(day17_copy,panels)

part1_sum = 0
robot_coords = None
robot_dir = None
for panel in panels:
    x = panel[0]
    y = panel[1]
    north = 0
    south = 0
    east = 0
    west = 0
    if (x,y-1) in panels and panels[(x,y-1)]['char'] in ['^', 'v', '<', '>', '#']: north = 1
    if (x,y+1) in panels and panels[(x,y+1)]['char'] in ['^', 'v', '<', '>', '#']: south = 1
    if (x+1,y) in panels and panels[(x+1,y)]['char'] in ['^', 'v', '<', '>', '#']: east = 1
    if (x-1,y) in panels and panels[(x-1,y)]['char'] in ['^', 'v', '<', '>', '#']: west = 1
    panels[panel]['north'] = north
    panels[panel]['south'] = south
    panels[panel]['east'] = east
    panels[panel]['west'] = west
    
    if panels[panel]['char'] in ['^', 'v', '<', '>']:
        panels[panel]['type'] = 'start'
        robot_coords = panel
        if panels[panel]['char'] == '^': robot_dir = 'N'
        elif panels[panel]['char'] == 'v': robot_dir = 'S'
        elif panels[panel]['char'] == '<': robot_dir = 'W'
        elif panels[panel]['char'] == '>': robot_dir = 'E'
    elif panels[panel]['char'] == '#' and north == 1 and south == 1 and east == 1 and west == 1:
        part1_sum += x*y
        panels[panel]['type'] = 'intersection'
    elif panels[panel]['char'] == '#' and ((north == 1 and south == 1) or (east == 1 and west == 1)):
        panels[panel]['type'] = 'straight'
    elif panels[panel]['char'] == '#' and ((north == 1 and (east == 1 or west == 1)) or (south == 1 and (east == 1 or west == 1))):
        panels[panel]['type'] = 'elbow'
    elif panels[panel]['char'] == '#' and (north == 1 or south == 1 or east == 1 or west == 1):
        panels[panel]['type'] = 'end'
                                          
print('Part 1:',part1_sum)

def determine_dir(panels,robot_coords,robot_dir):
    turn = ''
    if robot_dir == 'N' and panels[robot_coords]['north'] == 0:
        if panels[robot_coords]['east'] == 1:
            robot_dir = 'E'
            turn = 'R,'
        elif panels[robot_coords]['west'] == 1:
            robot_dir = 'W'
            turn = 'L,'
    elif robot_dir == 'S' and panels[robot_coords]['south'] == 0:
        if panels[robot_coords]['east'] == 1:
            robot_dir = 'E'
            turn = 'L,'
        elif panels[robot_coords]['west'] == 1:
            robot_dir = 'W'
            turn = 'R,'
    elif robot_dir == 'W' and panels[robot_coords]['west'] == 0:
        if panels[robot_coords]['north'] == 1:
            robot_dir = 'N'
            turn = 'R,'
        elif panels[robot_coords]['south'] == 1:
            robot_dir = 'S'
            turn = 'L,'
    elif robot_dir == 'E' and panels[robot_coords]['east'] == 0:
        if panels[robot_coords]['north'] == 1:
            robot_dir = 'N'
            turn = 'L,'
        elif panels[robot_coords]['south'] == 1:
            robot_dir = 'S'
            turn = 'R,'
    return robot_dir, turn

def move_robot(robot_coords,robot_dir):
    x = robot_coords[0]
    y = robot_coords[1]
    if robot_dir == 'N': y -= 1
    elif robot_dir == 'S': y += 1
    elif robot_dir == 'E': x += 1
    elif robot_dir == 'W': x -= 1
    robot_coords = (x,y)
    return robot_coords

#Trying to find a viable path, only turning at elbows for now
path = ''
moves = 0
while True:
    panels[robot_coords]['visited'] = 1
    if panels[robot_coords]['type'] == 'end':
        path += str(moves)
        print('Reached end!')
        print(path)
        break
    elif panels[robot_coords]['type'] == 'start':
        robot_dir, turn = determine_dir(panels,robot_coords,robot_dir)
        path += turn
        robot_coords = move_robot(robot_coords,robot_dir)
        moves += 1
    elif panels[robot_coords]['type'] in ['straight', 'intersection']:
        robot_coords = move_robot(robot_coords,robot_dir)
        moves += 1
    elif panels[robot_coords]['type'] == 'elbow':
        path += str(moves)+','
        moves = 0
        robot_dir, turn = determine_dir(panels,robot_coords,robot_dir)
        path += turn
        robot_coords = move_robot(robot_coords,robot_dir)
        moves += 1

#check that all scaffold panels were visited:
missed = 0
for panel in panels:
    if panels[panel]['char'] == '#' and panels[panel]['visited'] == 0:
        missed += 1
print('Scaffold panels missed:',missed)

#manually determined function patterns
main_str = 'A,A,B,B,C,B,C,B,C,A\n'
main_ascii = list()
for c in main_str:
    main_ascii.append(ord(c))
a_str = 'L,10,L,10,R,6\n'
a_ascii = list()
for c in a_str:
    a_ascii.append(ord(c))
b_str = 'R,12,L,12,L,12\n'
b_ascii = list()
for c in b_str:
    b_ascii.append(ord(c))
c_str = 'L,6,L,10,R,12,R,12\n'
c_ascii = list()
for c in c_str:
    c_ascii.append(ord(c))
video_str = 'n\n'
video_ascii = list()
for c in video_str:
    video_ascii.append(ord(c))
inputs = main_ascii + a_ascii + b_ascii + c_ascii + video_ascii

def run_part2(prog,inputs):
    pos = 0
    rel_base = 0
    stop = 0
    inpt = None
    input_count = 0
   
    while True:
        if str(prog[pos])[-1] == '3':
            inpt = inputs[input_count]
            input_count += 1
        stop, pos, outpt, rel_base = process_opcode(prog, pos, inpt, rel_base)
        
        if outpt != None:
            final_output = outpt
        if stop == 1:
            break
    
    return final_output


day17_copy = day17.copy()
#Force the vacuum robot to wake up by changing the value in your ASCII program at address 0 from 1 to 2
day17_copy[0] = 2
part2 = run_part2(day17_copy,inputs)
print('Part 2:',part2)