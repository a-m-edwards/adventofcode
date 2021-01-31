#Day 13 Part 1 and Part 2 Attempt 2
path = 'aoc2019_day13.txt'
day13 = dict()
index = 0
with open(path) as f:
    for l in f:
        for n in l.rstrip().split(','):
            day13[index] = int(n)
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

def render_image(panels,score):
    min_y = None
    max_y = None
    min_x = None
    max_x = None
    for panel in panels:
        if min_y == None or panel[1] < min_y: min_y = panel[1]
        if max_y == None or panel[1] > max_y: max_y = panel[1]
        if min_x == None or panel[0] < min_x: min_x = panel[0]
        if max_x == None or panel[0] > max_x: max_x = panel[0]
    print('Score: '+str(score))
    ball_x = None
    paddle_x = None
    blocks = 0
    for y in range(min_y,max_y+1):
        row = ''
        for x in range(min_x,max_x+1):
            if (x,y) in panels and panels[(x,y)]['tile_id'] == 1: row += 'W'
            elif (x,y) in panels and panels[(x,y)]['tile_id'] == 2: 
                row += '#'
                blocks += 1
            elif (x,y) in panels and panels[(x,y)]['tile_id'] == 3: 
                row += '~'
                paddle_x = x
            elif (x,y) in panels and panels[(x,y)]['tile_id'] == 4: 
                row += '*'
                ball_x = x
            else: row += ' '
        print(row)

def run_game(prog, quarters=None):
    pos = 0
    output_count = 0
    rel_base = 0
    x = None
    y = None
    score = None
    panels = dict()
    ball_x = None
    paddle_x = None
    
    def joystick_dir(ball_x,paddle_x):
        if ball_x != None and paddle_x != None and ball_x < paddle_x: joystick = -1
        elif ball_x != None and paddle_x != None and ball_x > paddle_x: joystick = 1
        else: joystick = 0
        return joystick
    
    if quarters != None:
        prog[0] = quarters
        
    while True:
        #print('Processing instruction at position '+str(pos))
        if int(str(prog[pos])[-1]) == 4: output_count += 1
        joystick = joystick_dir(ball_x,paddle_x)
        stop, pos, outpt, rel_base = process_opcode(prog, pos, joystick, rel_base)
        
        if outpt != None and output_count%3 == 1:
            x = outpt
        elif outpt != None and output_count%3 == 2:
            y = outpt
        elif outpt != None and output_count%3 == 0:
            if x == -1 and y == 0:
                score = outpt
                #print('Score: '+str(score))
            else:
                if (x,y) not in panels: 
                    panels[(x,y)] = dict()
                panels[(x,y)]['tile_id'] = outpt
                if outpt == 3: 
                    #print('Paddle is at '+str((x,y)))
                    paddle_x = x
                elif outpt == 4: 
                    #print('Ball is at '+str((x,y)))
                    ball_x = x
        if stop == 1: break
    
    render_image(panels,score)
    
    return panels, score

day13_part1 = day13.copy()
part1, score = run_game(day13_part1)
blocks = 0
for panel in part1:
    if part1[panel]['tile_id'] == 2: blocks += 1
print('Part 1 block tiles = '+str(blocks))

day13_part2 = day13.copy()
part2, score = run_game(day13_part2,quarters=2)
print('Part 2 score = '+str(score))
