#Day 16 Part 1 and Part 2
import tqdm

path = 'aoc2019_day16.txt'
day16 = list()
day16_txt = ''
with open(path) as f:
    for line in f:
        line = line.rstrip()
        day16 += [int(n) for n in line]
        day16_txt += line

test_txt = '03036732577212944063491565474664'
test = [int(n) for n in test_txt]

def get_pattern(length,position):
    base_pattern = [0, 1, 0, -1]
    new_pattern = list()
    for n in base_pattern:
        for i in range(1,position+1):
            new_pattern.append(n)
    final_pattern = new_pattern[1:]
    while len(final_pattern) < length:
        final_pattern += new_pattern
    final_pattern = final_pattern[:length]
    return final_pattern

def run_phase(inpt):
    inpt_len = len(inpt)
    new_inpt = list()
    for i in range(1,inpt_len+1):
        pat = get_pattern(inpt_len,i)
        result_list = [a*b for a,b in zip(inpt,pat)]
        result_num = 0
        for num in result_list:
            result_num += num
        new_inpt.append(int(str(result_num)[-1]))
    return new_inpt

part1_inpt = day16
phases = 100
for i in tqdm.trange(1,phases+1):
    part1_inpt = run_phase(part1_inpt)
part1 = ''
for i in range(0,8):
    part1 += str(part1_inpt[i])
print('Part 1:',part1)

part2_inpt = day16_txt
part2_txt = part2_inpt*10000
part2_start = int(part2_inpt[0:7])
part2_txt = part2_txt[part2_start:]
p2_phases = 100

for i in tqdm.trange(1,p2_phases+1):
    running_sum = 0
    new_str = ''
    for i in range(-1,-len(part2_txt)-1,-1):
        running_sum = running_sum + int(part2_txt[i])
        new_num = running_sum%10
        new_str = str(new_num)+new_str
    part2_txt = new_str
part2 = part2_txt[0:8]
print('Part 2:',part2)