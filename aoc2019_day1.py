#Day 1 Part 1 and Part 2
path = 'aoc2019_day1.txt'
with open(path) as f:
    modules = [int(x.rstrip()) for x in f]

def calc_fuel(mass):
    fuel = int(mass/3)-2
    return fuel

module_fuel = 0
for module in modules:
    module_fuel = module_fuel + calc_fuel(module)
print('Part 1 Fuel for Modules = '+str(module_fuel))

def calc_fuel_part2(mass):
    m_fuel = int(mass/3)-2
    f_fuel = 0
    fuel_input = m_fuel
    while True:
        add_fuel = int(fuel_input/3)-2
        if add_fuel <= 0: break
        f_fuel = f_fuel + add_fuel
        fuel_input = add_fuel
    total_fuel = m_fuel + f_fuel
    return total_fuel

part2_fuel = 0
for module in modules:
    part2_fuel = part2_fuel + calc_fuel_part2(module)
print('Part 2 Fuel for Modules and Fuel = '+str(part2_fuel))
