def run(filename):
    print('run file %s' % filename)
    with open(filename) as f:
        data = f.readlines()
        data = data[0].replace('\n', '')
        codes = data.split(',')
        codes = list(map(int, codes))
        input_val = 1

        # print(codes)
        original_codes = codes[:]

        res = part1(codes, input_val)
        print('part1 ans: %s' % res)

        input_val = 5
        res = part2(original_codes, input_val)
        print('part2 ans: %s' % res)

def part1(codes, input_val):
    idx = 0
    outputs = []
    while idx < len(codes):
        # print('idx', idx)
        ins = codes[idx]
        if ins == 99:
    	    return outputs

        ins_str = str(ins)
        if len(ins_str) < 5:
            ins_str = '0' * (5 - len(ins_str)) + ins_str
        # print(ins_str)
        op = int(ins_str[-2:])
        if op == 3:
            codes[codes[idx+1]] = input_val
            idx += 2
            continue
        if op == 4:
            if int(ins_str[-3]) == 0:
                outputs.append(codes[codes[idx+1]])
            else:
                outputs.append(codes[idx+1])
            idx += 2
            continue
        if op == 1 or op == 2:
            if int(ins_str[-3]) == 0:
                num1 = codes[codes[idx+1]]
            else:
                num1 = codes[idx+1]
            if int(ins_str[-4]) == 0:
                num2 = codes[codes[idx+2]]
            else:
                num2 = codes[idx+2]
            res = num1 + num2 if op == 1 else num1 * num2
            codes[codes[idx+3]] = res
            idx += 4
    return outputs

def part2(codes, input_val):
    idx = 0
    outputs = []
    while idx < len(codes):
        # print('idx', idx)
        ins = codes[idx]
        if ins == 99:
    	    return outputs

        ins_str = str(ins)
        if len(ins_str) < 5:
            ins_str = '0' * (5 - len(ins_str)) + ins_str
        # print(ins_str)
        op = int(ins_str[-2:])
        if op == 3:
            codes[codes[idx+1]] = input_val
            idx += 2
            continue
        if op == 4:
            if int(ins_str[-3]) == 0:
                outputs.append(codes[codes[idx+1]])
            else:
                outputs.append(codes[idx+1])
            idx += 2
            continue
        if int(ins_str[-3]) == 0:
            num1 = codes[codes[idx+1]]
        else:
            num1 = codes[idx+1]
        if int(ins_str[-4]) == 0:
            num2 = codes[codes[idx+2]]
        else:
            num2 = codes[idx+2]
        if op in [1, 2]:
            res = num1 + num2 if op == 1 else num1 * num2
            codes[codes[idx+3]] = res
            idx += 4
            continue
        if op == 5: # jump if true
            if num1 == 0:
                idx += 3
                continue
            idx = num2 # sets the instruction pointer to the value from the second parameter.
            continue
        if op == 6: # jump-if-false
            if num1 != 0:
                idx += 3
                continue
            idx = num2
            continue
        if op == 7: # less than
            codes[codes[idx+3]] = 1 if num1 < num2 else 0
            idx += 4
            continue
        if op == 8: # equal
            codes[codes[idx+3]] = 1 if num1 == num2 else 0
            idx += 4
            continue
    return outputs

if __name__ == '__main__':
    # run("input_test2")
    # run("input_test3")
    # run("input_test4")
    run("input")

