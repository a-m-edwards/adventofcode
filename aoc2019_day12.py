#Day 12 Part 1 and Part 2
import re
from itertools import combinations
import tqdm
import numpy as np

test1 = '''
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
'''

test2 = '''
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
'''

day12 = '''
<x=-1, y=7, z=3>
<x=12, y=2, z=-13>
<x=14, y=18, z=-8>
<x=17, y=4, z=-4>
'''

moon_id = 0
moons = dict()
text = day12
lines = text.strip().split('\n')
for line in lines:
    moon_id += 1
    moons[moon_id] = dict()
    moons[moon_id]['name'] = ['Io', 'Europa', 'Ganymede', 'Callisto'][moon_id-1]
    moons[moon_id]['pos_x'] = int(re.findall('x=(-*\d+),', line)[0])
    moons[moon_id]['pos_y'] = int(re.findall('y=(-*\d+),', line)[0])
    moons[moon_id]['pos_z'] = int(re.findall('z=(-*\d+)>', line)[0])
    moons[moon_id]['vel_x'] = 0
    moons[moon_id]['vel_y'] = 0
    moons[moon_id]['vel_z'] = 0

x_init = (moons[1]['pos_x'], moons[2]['pos_x'], moons[3]['pos_x'], moons[4]['pos_x'],0,0,0,0)
y_init = (moons[1]['pos_y'], moons[2]['pos_y'], moons[3]['pos_y'], moons[4]['pos_y'],0,0,0,0)
z_init = (moons[1]['pos_z'], moons[2]['pos_z'], moons[3]['pos_z'], moons[4]['pos_z'],0,0,0,0)
x_match = list()
y_match = list()
z_match = list()

coms = list(combinations([1,2,3,4],2))

def apply_gravity(moon1, moon2, dict_copy):
    def compare(dimension, moon1, moon2, dict_copy):
        pos = 'pos_'+dimension
        vel = 'vel_'+dimension
        if dict_copy[moon1][pos] > dict_copy[moon2][pos]:
            moons[moon1][vel] -= 1
            moons[moon2][vel] += 1
        elif dict_copy[moon1][pos] < dict_copy[moon2][pos]:
            moons[moon1][vel] += 1
            moons[moon2][vel] -= 1
    compare('x', moon1, moon2, dict_copy)
    compare('y', moon1, moon2, dict_copy)
    compare('z', moon1, moon2, dict_copy)

def apply_velocity(moon, dict_copy):
    moons[moon]['pos_x'] = dict_copy[moon]['pos_x'] + dict_copy[moon]['vel_x']
    moons[moon]['pos_y'] = dict_copy[moon]['pos_y'] + dict_copy[moon]['vel_y']
    moons[moon]['pos_z'] = dict_copy[moon]['pos_z'] + dict_copy[moon]['vel_z']

def find_match(i, init, current, match):
    if len(match) > 0: pass
    elif current == init:
        match.append(i)

for i in range(1,1000+1):
    dict_copy = moons.copy()
    for com in coms:
        apply_gravity(com[0], com[1], dict_copy)
    dict_copy = moons.copy()
    system_total = 0
    for moon in dict_copy:
        apply_velocity(moon, dict_copy)
        moons[moon]['pot'] = abs(moons[moon]['pos_x']) + abs(moons[moon]['pos_y']) + abs(moons[moon]['pos_z'])
        moons[moon]['kin'] = abs(moons[moon]['vel_x']) + abs(moons[moon]['vel_y']) + abs(moons[moon]['vel_z'])
        moons[moon]['total'] = moons[moon]['pot'] * moons[moon]['kin']
        system_total += moons[moon]['total']
    x_nums = (moons[1]['pos_x'], moons[2]['pos_x'], moons[3]['pos_x'], moons[4]['pos_x'],
             moons[1]['vel_x'], moons[2]['vel_x'], moons[3]['vel_x'], moons[4]['vel_x'])
    y_nums = (moons[1]['pos_y'], moons[2]['pos_y'], moons[3]['pos_y'], moons[4]['pos_y'],
             moons[1]['vel_y'], moons[2]['vel_y'], moons[3]['vel_y'], moons[4]['vel_y'])
    z_nums = (moons[1]['pos_z'], moons[2]['pos_z'], moons[3]['pos_z'], moons[4]['pos_z'],
             moons[1]['vel_z'], moons[2]['vel_z'], moons[3]['vel_z'], moons[4]['vel_z'])
    find_match(i, x_init, x_nums, x_match)
    find_match(i, y_init, y_nums, y_match)
    find_match(i, z_init, z_nums, z_match)

print('Part 1 sum of total energy = '+str(system_total))

for i in range(1001,200_000_000):
    if len(x_match) > 0 and len(y_match) > 0 and len(z_match) > 0: break
    dict_copy = moons.copy()
    for com in coms:
        apply_gravity(com[0], com[1], dict_copy)
    dict_copy = moons.copy()
    for moon in dict_copy:
        apply_velocity(moon, dict_copy)
    x_nums = (moons[1]['pos_x'], moons[2]['pos_x'], moons[3]['pos_x'], moons[4]['pos_x'],
             moons[1]['vel_x'], moons[2]['vel_x'], moons[3]['vel_x'], moons[4]['vel_x'])
    y_nums = (moons[1]['pos_y'], moons[2]['pos_y'], moons[3]['pos_y'], moons[4]['pos_y'],
             moons[1]['vel_y'], moons[2]['vel_y'], moons[3]['vel_y'], moons[4]['vel_y'])
    z_nums = (moons[1]['pos_z'], moons[2]['pos_z'], moons[3]['pos_z'], moons[4]['pos_z'],
             moons[1]['vel_z'], moons[2]['vel_z'], moons[3]['vel_z'], moons[4]['vel_z'])
    find_match(i, x_init, x_nums, x_match)
    find_match(i, y_init, y_nums, y_match)
    find_match(i, z_init, z_nums, z_match)
print('x match: '+str(x_match))
print('y match: '+str(y_match))
print('z match: '+str(z_match))

arr = np.array([x_match[0], y_match[0], z_match[0]], dtype='int64')
lcm = np.lcm.reduce(arr)
print('Part 2 number of steps it takes to return to the initial state = '+str(lcm))