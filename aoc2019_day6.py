#Day 6 Part 1 and Part 2
path = 'aoc2019_day6.txt'
objects = dict()
with open(path) as f:
    for l in f:
        x = l.rstrip().split(')')
        objects[x[1]] = dict()
        objects[x[1]]['orbit'] = x[0]
        objects[x[1]]['checksum'] = None

while True:
    updates = 0
    for obj in objects:
        orbit = objects[obj]['orbit']
        if objects[obj]['checksum'] != None: 
            continue
        elif orbit == 'COM': 
            objects[obj]['checksum'] = 1
            updates += 1
        elif objects[orbit]['checksum'] != None: 
            objects[obj]['checksum'] = objects[orbit]['checksum'] + 1
            updates += 1
    if updates == 0: break

orbits = 0
for obj in objects:
    orbits += objects[obj]['checksum']
print('Part 1 total direct and indirect orbits = '+str(orbits))

#chart path from YOU to COM
you_orbit = objects['YOU']['orbit']
obj = you_orbit
you_pathtoCOM = list()
while True:
    you_pathtoCOM.append(obj)
    if obj == 'COM': break
    next_obj = objects[obj]['orbit']
    obj =  next_obj

#chart path from SAN to COM
san_orbit = objects['SAN']['orbit']
obj = san_orbit
san_pathtoCOM = list()
while True:
    san_pathtoCOM.append(obj)
    if obj == 'COM': break
    next_obj = objects[obj]['orbit']
    obj =  next_obj

#find first common object in the 2 paths
branch = None
for obj in you_pathtoCOM:
    if obj in san_pathtoCOM:
        branch = obj
    if branch != None: break

transfers = (objects[you_orbit]['checksum']-objects[branch]['checksum'])+(objects[san_orbit]['checksum']-objects[branch]['checksum'])
print('Part 2 orbital transfers = '+str(transfers))