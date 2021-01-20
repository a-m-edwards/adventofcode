#Day 10 Part 1 and Part 2
from itertools import permutations
import math

path = 'aoc2019_day10.txt'
x = 0
y = 0
asteroids = dict()
with open(path) as f:
    for l in f:
        l = l.rstrip()
        x = 0
        for c in l:
            if c == '#': asteroids[(x,y)] = dict()
            x += 1
        y += 1

perms = {index : dict() for index in list(permutations(asteroids.keys(), 2))}
for perm in perms:
    x1 = perm[0][0]
    y1 = perm[0][1]
    x2 = perm[1][0]
    y2 = perm[1][1]
    rise = y2 - y1
    run = x2 - x1
    if run == 0:
        m = None
        b = None
        a = x1
    else:
        m = rise/run
        b = y1 - m * x1
        a = None
    if rise < 0: ydir = 'negative'
    elif rise == 0: ydir = 'zero'
    else: ydir = 'positive'
    if run < 0: xdir = 'negative'
    elif run == 0: xdir = 'zero'
    else: xdir = 'positive'
    perms[perm]['line_eq'] = (m, b, a, ydir, xdir)
    perms[perm]['distance'] = math.sqrt(rise**2 + run**2)
    
max_count = None
best_coord = None
for asteroid in asteroids:
    line_eqs = set()
    for perm in perms:
        if asteroid == perm[0]:
            line_eqs.add(perms[perm]['line_eq'])
    asteroids[asteroid]['count'] = len(line_eqs)
    asteroids[asteroid]['vaporized'] = None
    if max_count == None or max_count < len(line_eqs):
        max_count = len(line_eqs)
        best_coords = asteroid
print('Part 1 best is '+str(best_coords)+' with '+str(max_count)+' other asteroids detected')

part2 = dict()
for perm in perms:
    if best_coords == perm[0]:
        line_eq = perms[perm]['line_eq']
        distance = perms[perm]['distance']
        if line_eq not in part2:
            part2[line_eq] = dict()
            part2[line_eq]['asteroids'] = list()
            part2[line_eq]['asteroids'].append((distance, perm[1]))
        else: part2[line_eq]['asteroids'].append((distance, perm[1]))

up = list()
up_right = list()
right = list()
down_right = list()
down = list()
down_left = list()
left = list()
up_left = list()
for item in part2:
    part2[item]['asteroids'].sort()
    if item[3] == 'negative' and item[4] == 'zero':
        up.append(item)
    elif item[3] == 'negative' and item[4] == 'positive':
        up_right.append(item)
    elif item[3] == 'zero' and item[4] == 'positive':
        right.append(item)
    elif item[3] == 'positive' and item[4] == 'positive':
        down_right.append(item)
    elif item[3] == 'positive' and item[4] == 'zero':
        down.append(item)
    elif item[3] == 'positive' and item[4] == 'negative':
        down_left.append(item)
    elif item[3] == 'zero' and item[4] == 'negative':
        left.append(item)
    elif item[3] == 'negative' and item[4] == 'negative':
        up_left.append(item)

def return_m(item):
    return abs(item[0])

up_right.sort(key=return_m, reverse=True)
down_right.sort(key=return_m)
down_left.sort(key=return_m, reverse=True)
up_left.sort(key=return_m)

line_eqs = up+up_right+right+down_right+down+down_left+left+up_left

while True:
    updates = 0
    vaporized = 0
    for eq in line_eqs:
        if len(part2[eq]['asteroids']) == 0: continue
        vaporized += 1
        asteroid = part2[eq]['asteroids'][0][1]
        asteroids[asteroid]['vaporized'] = vaporized
        part2[eq]['asteroids'].pop(0)
        updates += 1
        if vaporized == 200: ast_200 = asteroid
    if updates == 0: break

print('Part 2 '+str(ast_200)+' is the 200th to be vaporized. x * 100 + y = '+str(ast_200[0]*100+ast_200[1]))