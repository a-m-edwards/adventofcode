#Day 15 Part 1 and Part 2
from itertools import permutations
import copy

path = 'aoc2019_day15.txt'
day15 = dict()
index = 0
with open(path) as f:
    for l in f:
        for n in l.rstrip().split(','):
            day15[index] = int(n)
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

def render_image(panels,droid_x,droid_y):
    min_y = None
    max_y = None
    min_x = None
    max_x = None
    for panel in panels:
        if min_y == None or panel[1] < min_y: min_y = panel[1]
        if max_y == None or panel[1] > max_y: max_y = panel[1]
        if min_x == None or panel[0] < min_x: min_x = panel[0]
        if max_x == None or panel[0] > max_x: max_x = panel[0]
    for y in range(max_y,min_y-1,-1):
        row = ''
        for x in range(min_x,max_x+1):
            if (x,y) == (droid_x,droid_y): row += 'D' #droid
            elif (x,y) == (0,0): row += '*' #starting location
            elif (x,y) in panels and panels[(x,y)]['type'] == 0: row += '#' #wall
            elif (x,y) in panels and panels[(x,y)]['type'] == 1: 
                if panels[(x,y)]['oxygen'] == 0: row += '.' #viable path
                elif panels[(x,y)]['oxygen'] == 1: row += 'o' #viable path
            elif (x,y) in panels and panels[(x,y)]['type'] == 2: row += 'O' #oxygen system
            elif (x,y) in panels and panels[(x,y)]['type'] == 3: row += 'X' #deadend
            else: row += ' '
        print(row)

def determine_dir(panels,droid_x,droid_y,dirs):
    
    def panel_coords(dir_num,droid_x,droid_y):
        if dir_num == 1: #north
            panel_x = droid_x
            panel_y = droid_y+1
        elif dir_num == 2: #south
            panel_x = droid_x
            panel_y = droid_y-1
        elif dir_num == 3: #west
            panel_x = droid_x-1
            panel_y = droid_y
        elif dir_num == 4: #east
            panel_x = droid_x+1
            panel_y = droid_y
        return (panel_x,panel_y)
    
    panel_coords0 = panel_coords(dirs[0],droid_x,droid_y)
    panel_coords1 = panel_coords(dirs[1],droid_x,droid_y)
    panel_coords2 = panel_coords(dirs[2],droid_x,droid_y)
    panel_coords3 = panel_coords(dirs[3],droid_x,droid_y)
    
    #First try to find an unmapped panel
    if panel_coords0 not in panels:
        direction = dirs[0]
    elif panel_coords1 not in panels:
        direction = dirs[1]
    elif panel_coords2 not in panels:
        direction = dirs[2]
    elif panel_coords3 not in panels:
        direction = dirs[3]
        
    #If all panels are mapped, find a direction that isn't a wall or a deadend (code 3)
    elif panels[panel_coords0]['type'] not in [0,3]:
        direction = dirs[0]
    elif panels[panel_coords1]['type'] not in [0,3]:
        direction = dirs[1]
    elif panels[panel_coords2]['type'] not in [0,3]:
        direction = dirs[2]
    elif panels[panel_coords3]['type'] not in [0,3]:
        direction = dirs[3]

    #If all panels are walls or deadends, pick a direction that is not a wall
    elif panels[panel_coords0]['type'] != 0:
        direction = dirs[0]
    elif panels[panel_coords1]['type'] != 0:
        direction = dirs[1]
    elif panels[panel_coords2]['type'] != 0:
        direction = dirs[2]
    elif panels[panel_coords3]['type'] != 0:
        direction = dirs[3]
    
    #set panel x,y based on direction
    if direction == dirs[0]:
        panel_x = panel_coords0[0]
        panel_y = panel_coords0[1]
    elif direction == dirs[1]:
        panel_x = panel_coords1[0]
        panel_y = panel_coords1[1]
    elif direction == dirs[2]:
        panel_x = panel_coords2[0]
        panel_y = panel_coords2[1]
    elif direction == dirs[3]:
        panel_x = panel_coords3[0]
        panel_y = panel_coords3[1]
        
    return direction, panel_x, panel_y

def deadend_check(panels,panel_x,panel_y):
    #If a panel is surrounded by 3 walls or other deadends, will mark the panel as a deadend (code 3)
    obstructions = 0
    #north
    if (panel_x,panel_y+1) in panels and panels[(panel_x,panel_y+1)]['type'] in [0,3]:
        obstructions += 1
    #south
    if (panel_x,panel_y-1) in panels and panels[(panel_x,panel_y-1)]['type'] in [0,3]:
        obstructions += 1
    #west
    if (panel_x-1,panel_y) in panels and panels[(panel_x-1,panel_y)]['type'] in [0,3]:
        obstructions += 1
    #east
    if (panel_x+1,panel_y) in panels and panels[(panel_x+1,panel_y)]['type'] in [0,3]:
        obstructions += 1
    
    if obstructions >= 3: 
        deadend = 1
    else: deadend = 0
        
    if deadend == 1: 
        if (panel_x,panel_y) not in panels: 
            panels[(panel_x,panel_y)] = dict()
        panels[(panel_x,panel_y)]['type'] = 3
    
    return panels
        
def run_droid(panels,move_dict,prog,test):
    pos = 0
    rel_base = 0
    droid_x = 0
    droid_y = 0
    panel_x = None
    panel_y = None
    render = 0
    moves = 0
    global_moves = 0
    
    def update_move_dict(move_dict,global_moves,panel_x,panel_y,panel_type):
        if (panel_x,panel_y) not in move_dict: 
            move_dict[(panel_x,panel_y)] = dict()
            move_dict[(panel_x,panel_y)]['moves'] = None
            move_dict[(panel_x,panel_y)]['type'] = panel_type
            move_dict[(panel_x,panel_y)]['oxygen'] = 0
        if move_dict[(panel_x,panel_y)]['type'] != 0:
            if move_dict[(panel_x,panel_y)]['moves'] == None or global_moves < move_dict[(panel_x,panel_y)]['moves']:
                move_dict[(panel_x,panel_y)]['moves'] = global_moves
            elif global_moves > move_dict[(panel_x,panel_y)]['moves']:
                global_moves = move_dict[(panel_x,panel_y)]['moves']
        return move_dict,global_moves
        
    while True:
        direction, panel_x, panel_y = determine_dir(panels,droid_x,droid_y,test)
        stop, pos, outpt, rel_base = process_opcode(prog, pos, direction, rel_base)
        
        #0: The repair droid hit a wall. Its position has not changed.
        if outpt == 0:
            #Add/update panels dict
            if (panel_x,panel_y) not in panels: 
                panels[(panel_x,panel_y)] = dict()
            panels[(panel_x,panel_y)]['type'] = 0
            #Add/update move_dict
            move_dict,global_moves = update_move_dict(move_dict,global_moves,panel_x,panel_y,0)
            #check if droid is sitting on a deadend panel
            panels = deadend_check(panels,droid_x,droid_y)
        #1: The repair droid has moved one step in the requested direction.
        elif outpt == 1:
            moves += 1
            global_moves += 1
            #Add/update panels dict
            #only mark as type 1 if not already in panels, as we don't want to overwrite deadends
            if (panel_x,panel_y) not in panels: 
                panels[(panel_x,panel_y)] = dict()
                panels[(panel_x,panel_y)]['type'] = 1
            panels[(panel_x,panel_y)]['moves'] = moves
            #Add/update move_dict
            move_dict,global_moves = update_move_dict(move_dict,global_moves,panel_x,panel_y,1)
            droid_x,droid_y = panel_x,panel_y
            #check if droid is sitting on a deadend panel
            panels = deadend_check(panels,droid_x,droid_y)
        #2: The repair droid has moved one step in the requested direction; 
        #its new position is the location of the oxygen system.
        elif outpt == 2:
            moves += 1
            global_moves += 1
            #Add/update panels dict
            if (panel_x,panel_y) not in panels: 
                panels[(panel_x,panel_y)] = dict()
            panels[(panel_x,panel_y)]['type'] = 2
            panels[(panel_x,panel_y)]['moves'] = moves
            #Add/update move_dict
            move_dict,global_moves = update_move_dict(move_dict,global_moves,panel_x,panel_y,2)
            droid_x,droid_y = panel_x,panel_y
            stop = 1
        if outpt != None: 
            render += 1
            #print('*****RENDER: ',render)
            #render_image(panels,droid_x,droid_y)
            #print('\n')
        if stop == 1: break
    
    return panels, move_dict, droid_x, droid_y

#Determine every permutation of the order in which to check directions
possible_dirs = [1,2,3,4]
perms = list(permutations(possible_dirs))

move_dict = dict()
for i in range(0,len(perms)):
    perm_dict = dict()
    print('***** PART 1 PERMUTATION',i,'*****')
    day15_copy = day15.copy()
    perm_dict, move_dict, droid_x, droid_y = run_droid(perm_dict,move_dict,day15_copy,perms[i])
    print('Permutation',i,'found oxygen system at',(droid_x,droid_y),'in',perm_dict[(droid_x,droid_y)]['moves'],'moves')
    print('Fewest moves per global moves dict:',move_dict[(droid_x,droid_y)]['moves'])
print('\n','Part 1 fewest moves:',move_dict[(droid_x,droid_y)]['moves'],'\n')
print('***** FINAL PART 1 MAP ******')
render_image(move_dict,droid_x,droid_y)

minutes = 0
move_dict[(droid_x,droid_y)]['oxygen'] = 1
while True:
    updates = 0
    dict_copy = copy.deepcopy(move_dict)
    for panel in dict_copy:
        if dict_copy[panel]['type'] == 0: continue
        elif dict_copy[panel]['oxygen'] == 1: continue
        else:
            if (dict_copy[(panel[0],panel[1]+1)]['oxygen'] == 1
                or dict_copy[(panel[0],panel[1]-1)]['oxygen'] == 1
                or dict_copy[(panel[0]-1,panel[1])]['oxygen'] == 1
                or dict_copy[(panel[0]+1,panel[1])]['oxygen'] == 1):
                updates += 1
                move_dict[panel]['oxygen'] = 1
    if updates > 0:
        minutes += 1
        #print('\n','******PART 2 RENDER for MINUTE',minutes,'with',updates,'updates*****')
        #render_image(move_dict,droid_x,droid_y)
    elif updates == 0:
        print('\n','Part 2 area filled with oxygen in',minutes,'minutes','\n')
        break

print('***** FINAL PART 2 MAP ******')
render_image(move_dict,droid_x,droid_y)