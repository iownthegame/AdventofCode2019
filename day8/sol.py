def run():
    width = 25
    height = 6
    filename = "input"

    # width = 2
    # height = 2
    # filename = "input_test"

    with open(filename) as f:
        data = f.readlines()
        data = data[0].replace('\n', '')

        res = part1(data, width, height)
        print('part1 ans: %s' % res)

        res = part2(data, width, height)
        print('part2 ans:')
	for i in range(0, len(res), width):
            print(''.join(res[i:i+width]).replace('1', 'X').replace('0', ' '))

def part1(data, width, height):
    length = width * height
    min_zero_cnt = float('inf')
    result = None
    for i in range(0, len(data), length):
	current_layer = data[i:i+length]
        zero_cnt = current_layer.count('0')
        if zero_cnt < min_zero_cnt:
            min_zero_cnt = zero_cnt
            result = current_layer.count('1') * current_layer.count('2')
    return result

def part2(data, width, height):
    length = width * height
    layers = []
    for i in range(0, len(data), length):
	current_layer = data[i:i+length]
	layers.append(current_layer)
    len_layers = len(layers)
    res = []
    # print(layers)
    for i in range(length):
        for j in range(len_layers):
            if layers[j][i] != '2':
                res.append(layers[j][i])
                break
        else:
            res.append('2') # all are '2' transparent
    return res       

if __name__ == '__main__':
    run()

