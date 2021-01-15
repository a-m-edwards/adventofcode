#Day 8 Part 1
path = 'aoc2019_day8.txt'
digits = ''
with open(path) as f:
    for l in f:
        digits = digits + l.rstrip()
width = 25
height = 6
layer_len = int(width*height)
layer_count = int(len(digits)/layer_len)
layers = dict()
lstart = 0
lstop = layer_len
for layer in range(1,layer_count+1):
    layers[layer] = dict()
    layers[layer]['digits'] = digits[lstart:lstop]
    rstart = 0
    rstop = width
    for row in range(1,height+1):
        layers[layer][row] = layers[layer]['digits'][rstart:rstop]
        rstart += width
        rstop += width
    zeros = 0
    ones = 0
    twos = 0
    for d in layers[layer]['digits']:
        if int(d) == 0: zeros += 1
        elif int(d) == 1: ones += 1
        elif int(d) == 2: twos += 1
    layers[layer]['zeros'] = zeros
    layers[layer]['product'] = ones*twos
    lstart += layer_len
    lstop += layer_len

least_zeros = None
for layer in layers:
    if least_zeros == None or least_zeros > layers[layer]['zeros']:
        least_zeros = layers[layer]['zeros']
        part1_layer = layer
print('Part 1 product of 1 and 2 digits = '+str(layers[part1_layer]['product']))

#Part 2
#0 is black, 1 is white, and 2 is transparent
#layers are rendered with the first layer in front and the last layer in back
image = dict()
for row in range(1,height+1):
    image[row] = [int(d) for d in layers[1][row]]
for layer in range(2,layer_count+1):
    for row in range(1,height+1):
        for d in range(0,width):
            if image[row][d] in [0,1]: continue
            elif int(layers[layer][row][d]) == 2: continue
            elif image[row][d] == 2 and int(layers[layer][row][d]) in [0,1]:
                image[row][d] = int(layers[layer][row][d])
for row in range(1,height+1):
    print(image[row])