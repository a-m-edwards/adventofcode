#Day 4 Part 1 and Part 2
import re

def part1_check(num):
    valid = 0
    double = 0
    decrease = 0
    num_str = str(num)
    
    for i in range(0,len(num_str)-1):
        #Two adjacent digits are the same
        if num_str[i+1] == num_str[i]: double = 1
        #Going from left to right, the digits never decrease
        if int(num_str[i+1]) < int(num_str[i]): decrease = 1
    
    if double == 1 and decrease == 0: valid = 1
    return valid

def part2_check(num):
    valid = 0
    double = 0
    decrease = 0
    num_str = str(num)
    
    #Two adjacent digits are the same and the two adjacent matching digits are not part of a larger group of matching digits
    regex = re.findall('0{2,}|1{2,}|2{2,}|3{2,}|4{2,}|5{2,}|6{2,}|7{2,}|8{2,}|9{2,}', num_str)
    if len(regex) > 0:
        for match in regex:
            if len(match) == 2: double = 1
    
    for i in range(0,len(num_str)-1):
        #Going from left to right, the digits never decrease
        if int(num_str[i+1]) < int(num_str[i]): decrease = 1
    
    if double == 1 and decrease == 0: valid = 1
    return valid

part1_count = 0
part2_count = 0
for i in range(278384,824795+1):
    part1_count = part1_count + part1_check(i)
    part2_count = part2_count + part2_check(i)

print('Part 1 valid passwords = '+str(part1_count))
print('Part 2 valid passwords = '+str(part2_count))