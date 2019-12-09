def run(filename, alarm=False):
    print('run file %s' % filename)
    with open(filename) as f:
        data = f.readlines()
	data = data[0].replace('\n', '')
        codes = data.split(',')
        codes = list(map(int, codes))
        original_codes = codes[:]

        res = part1(codes, alarm)
        print('part1 ans: %s' % res)

        res = part2(original_codes)
        print('part2 ans: %s' % res)

def part1(codes, alarm):
    if alarm: # restore the gravity assist program to the "1202 program alarm
        codes[1] = 12
        codes[2] = 2
    idx = 0
    while idx < len(codes):
        op = codes[idx]
        if op == 99:
	    return codes
        num1 = codes[codes[idx+1]]
        num2 = codes[codes[idx+2]]
        res = num1 + num2 if op == 1 else num1 * num2
        codes[codes[idx+3]] = res
	idx += 4
    return codes

def part2(codes):
    original_codes = codes[:]
    target = 19690720
    for noun in range(100):
        for verb in range(100):
            codes = original_codes[:]
            codes[1] = noun
            codes[2] = verb
            try:
                res = part1(codes, False)
                # print('noun = %s, verb = %s, res = %s' % (noun, verb, res[0]))
                if res[0] == target:
                    return noun * 100 + verb
            except Exception as e:
                # print('noun = %s, verb = %s, res = %s' % (noun, verb, -1))
                continue

if __name__ == '__main__':
    # run("input_test1")
    # run("input_test2")
    # run("input_test3")
    # run("input_test4")
    # run("input_test5")
    run("input", True)

