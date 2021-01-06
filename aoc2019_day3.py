#Day 3 Part 1 and Part 2
path = 'aoc2019_day3.txt'
line_count = 0
with open(path) as f:
    for line in f:
        line_count = line_count + 1
        if line_count == 1:
            wire1_inst = line.rstrip().split(',')
        elif line_count == 2:
            wire2_inst = line.rstrip().split(',')

wire1_coord = dict()            
wire1_coord[(0,0)] = dict()
wire1_coord[(0,0)]['distance'] = 0
wire1_coord[(0,0)]['steps'] = 0
wire2_coord = dict() 
wire2_coord[(0,0)] = dict()
wire2_coord[(0,0)]['distance'] = 0
wire2_coord[(0,0)]['steps'] = 0
def chart_path(inst, wire, x, y, steps):
    if wire == 1:
        coord = wire1_coord
    elif wire == 2:
        coord = wire2_coord
    dr = inst[0]
    dist = int(inst[1:])
    x_start = x
    y_start = y
    def update_dict(x,y):
        if (x,y) not in coord:
            coord[(x,y)] = dict()
            coord[(x,y)]['distance'] = abs(x)+abs(y)
            coord[(x,y)]['steps'] = steps
    if dr == 'L':
        for i in range(x_start-1,x_start-dist-1,-1):
            x = i
            steps = steps + 1
            update_dict(x,y)
    elif dr == 'R':
        for i in range(x_start+1,x_start+dist+1):
            x = i
            steps = steps + 1
            update_dict(x,y)
    elif dr == 'U':
        for i in range(y_start+1,y_start+dist+1):
            y = i
            steps = steps + 1
            update_dict(x,y)
    elif dr == 'D':
        for i in range(y_start-1,y_start-dist-1,-1):
            y = i
            steps = steps + 1
            update_dict(x,y)
    return x,y,steps

x,y,steps = 0,0,0  
for inst in wire1_inst:
    x,y,steps = chart_path(inst,1,x,y,steps)
x,y,steps = 0,0,0 
for inst in wire2_inst:
    x,y,steps = chart_path(inst,2,x,y,steps)
    
part1 = list()
part2 = list()
for coord in wire1_coord:
    if coord in wire2_coord:
        part1.append((wire2_coord[coord]['distance'],coord))
        part2.append((wire1_coord[coord]['steps']+wire2_coord[coord]['steps'],coord))
part1.sort()
part2.sort()
print('Part 1 distance = '+str(part1[1][0]))
print('Part 2 steps = '+str(part2[1][0]))