#Day 14 Part 1 and Part 2
import re, math, tqdm

path = 'aoc2019_day14.txt'
day14_lines = list()
with open(path) as f:
    for line in f:
        line = line.rstrip()
        day14_lines.append(line)

test_txt = '''
171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX
'''
test_lines = test_txt.strip().split('\n')

lines = day14_lines
chems = dict()
for line in lines:
    regex1 = re.findall('=> (\d+) ([A-Z]+)$',line)
    chem = regex1[0][1]
    min_qty = regex1[0][0]
    regex2 = re.findall('^(.+) =>',line)
    inpt = regex2[0]
    inputs = inpt.split(',')
    input_list = list()
    ore_cost = 0
    for item in inputs:
        item = item.strip()
        regex3 = re.findall('^(\d+) ([A-Z]+)$',item)
        input_list.append((regex3[0][1], int(regex3[0][0])))
        if regex3[0][1] == 'ORE': 
            ore_cost = int(regex3[0][0])
    chems[chem] = dict()
    chems[chem]['min qty'] = int(min_qty)
    chems[chem]['input'] = input_list
    chems[chem]['p1_need'] = 0
    chems[chem]['p1_produced'] = 0
    chems[chem]['p1_extra'] = 0
    chems[chem]['p2_need'] = 0
    chems[chem]['p2_produced'] = 0
    chems[chem]['p2_extra'] = 0
    chems[chem]['ore cost'] = ore_cost

def make_fuel(fuel_amount,part):
    total_ore_cost = 0
    need_label = part+'_need'
    prod_label = part+'_produced'
    extra_label = part+'_extra'
    
    #Make a list of the amount of inputs we need for the specified fuel amount
    fuel_inputs = list()
    for item in chems['FUEL']['input']:
        chem = item[0]
        qty = item[1]*fuel_amount
        fuel_inputs.append((chem,qty))
    fuel_copy = fuel_inputs.copy()
    
    #Produce initial set of fuel inputs, enter results into chems dict
    for item in fuel_copy:
        fuel_inputs.remove(item)
        chem = item[0]
        want = item[1]
        chems[chem][need_label] += want
        min_qty = chems[chem]['min qty']
        prod_runs = math.ceil(want/min_qty)
        prod_qty = prod_runs*min_qty
        extra = prod_qty - want
        chems[chem][prod_label] += prod_qty
        chems[chem][extra_label] = extra
        cost = prod_runs*chems[chem]['ore cost']
        total_ore_cost += cost
        #If the fuel input doesn't come from ore, add it to the list of fuel inputs again for later reduction
        if chems[chem]['ore cost'] == 0:
            fuel_inputs.append((chem,prod_qty))

    #Reduce any fuel inputs that don't come from ore into their component ingredients and produce them
    #Enter the results of the produced chemicals in the chems dict
    while True:
        updates = 0
        fuel_copy = fuel_inputs.copy()
        for item in fuel_copy:
            fuel_inputs.remove(item)
            parent_chem = item[0]
            parent_qty = item[1]
            parent_min_qty = chems[parent_chem]['min qty']
            parent_prod_runs = parent_qty/parent_min_qty
            #Skip any fuel inputs that come from ore, as their cost was already calculated at production
            if chems[parent_chem]['ore cost'] > 0: continue
            else:
                updates += 1
                for child in chems[parent_chem]['input']:
                    child_chem = child[0]
                    child_qty = child[1]
                    want = parent_prod_runs*child_qty
                    have = chems[child_chem][extra_label]
                    need = want - have 
                    chems[child_chem][need_label] += want
                    if need <= 0:
                        chems[child_chem][extra_label] = have - want
                    elif need > 0:
                        child_min_qty = chems[child_chem]['min qty']
                        child_prod_runs = math.ceil(need/child_min_qty)
                        child_prod_qty = child_prod_runs*child_min_qty
                        extra = child_prod_qty - need
                        chems[child_chem][prod_label] += child_prod_qty
                        chems[child_chem][extra_label] = extra
                        cost = child_prod_runs*chems[child_chem]['ore cost']
                        total_ore_cost += cost
                        fuel_inputs.append((child_chem,child_prod_qty))
        if updates == 0: break
    
    return total_ore_cost

part1_ore = make_fuel(1,'p1')
print('Part 1 min ORE to produce 1 FUEL = '+str(part1_ore))

#Per hints I found online doing a binary search pattern to try guessing the fuel amount
upper_bound = None
lower_bound = 1
part2_ore = 1_000_000_000_000
guesses = 0
while lower_bound+1 != upper_bound:
    if upper_bound == None:
        guess = lower_bound*2
    else:
        guess = (upper_bound+lower_bound)//2
    
    ore_needed = make_fuel(guess,'p2')
    guesses += 1
    if ore_needed > part2_ore:
        upper_bound = guess
    else:
        lower_bound = guess
        
print('Part 2 FUEL produced by 1_000_000_000_000 ORE = '+str(lower_bound))
