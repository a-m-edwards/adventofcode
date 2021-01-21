#Day 11 Part 1 and Part 2
path = 'aoc2019_day11.txt'
day11 = dict()
index = 0
with open(path) as f:
    for l in f:
        for n in l.rstrip().split(','):
            day11[index] = int(n)
            index += 1
    
def process_opcode(position, input1, input2, input_count, output_count, prog, rel_base):
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
        output_count += 1
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
    
    return stop, new_pos, input_count, outpt, output_count, rel_base

def run_robot(inpt, prog):
    prog_copy = prog.copy()
    pos = 0
    input_count = 0
    output_count = 0
    rel_base = 0
    panels = dict()
    x,y = 0,0
    #The robot starts facing up.
    robot_dir = 0
    #provide 0 if the robot is over a black panel or 1 if the robot is over a white panel
    panels[(x,y)] = dict()
    panels[(x,y)]['color'] = inpt
    panels[(x,y)]['times painted'] = 0
    while True:
        #print('Processing instruction at position '+str(pos))
        stop, pos, input_count, outpt, output_count, rel_base = process_opcode(pos, inpt, inpt, input_count, output_count, prog_copy, rel_base)
        
        #First, it will output a value indicating the color to paint the panel the robot is over: 
        #0 means to paint the panel black, and 1 means to paint the panel white.
        if outpt != None and output_count%2 != 0:
            panels[(x,y)]['color'] = outpt
            panels[(x,y)]['times painted'] += 1
            #print(str((x,y))+' painted!')
        #Second, it will output a value indicating the direction the robot should turn: 
        #0 means it should turn left 90 degrees, and 1 means it should turn right 90 degrees.
        #After the robot turns, it should always move forward exactly one panel.
        elif outpt != None and output_count%2 == 0:
            if outpt == 0:
                robot_dir = (robot_dir-90)%360
            elif outpt == 1:
                robot_dir = (robot_dir+90)%360
            if robot_dir == 0: y += 1
            elif robot_dir == 90: x += 1
            elif robot_dir == 180: y -= 1
            elif robot_dir == 270: x -= 1
            if (x,y) not in panels: 
                panels[(x,y)] = dict()
                panels[(x,y)]['color'] = 0
                panels[(x,y)]['times painted'] = 0
            inpt = panels[(x,y)]['color']
            #print('output = '+str(outpt)+', new robot_dir = '+str(robot_dir)+', new x,y = '+str((x,y)))
        if stop == 1: break
    return panels

#Part 1: All of the panels are currently black.
part1 = run_robot(0, day11)
panels_painted = 0
for panel in part1:
    if part1[panel]['times painted'] > 0: panels_painted += 1
print('Part 1 '+str(panels_painted)+' panels are painted at least once')

#Part 2: starting the robot on a single white panel
part2 = run_robot(1, day11)
min_y = None
max_y = None
min_x = None
max_x = None
for panel in part2:
    if min_y == None or panel[1] < min_y: min_y = panel[1]
    if max_y == None or panel[1] > max_y: max_y = panel[1]
    if min_x == None or panel[0] < min_x: min_x = panel[0]
    if max_x == None or panel[0] > max_x: max_x = panel[0]
image = list()
for y in range(max_y,min_y-1,-1):
    row = ''
    for x in range(min_x,max_x+1):
        if (x,y) in part2 and part2[(x,y)]['color'] == 1: row += '#'
        else: row += '.'
    image.append(row)
    print(row)