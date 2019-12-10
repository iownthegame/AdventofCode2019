def run(filename):
    print('run file %s' % filename)
    with open(filename) as f:
        data = f.readlines()
        data = data[0].replace('\n', '')
        codes = data.split(',')
        codes = list(map(int, codes))
        original_codes = codes[:]

        # print(codes)

        res = part1(codes)
        print('part1 ans: %s' % res)

        res = part2(original_codes)
        print('part2 ans: %s' % res)

def day5(codes, input_val, idx=0, return_on_output=False):
    """
    The computer's available memory should be much larger than the initial program. Memory beyond the initial program starts with the value 0 and can be read or written like any other memory.
    """
    # change codes array to dictionary
    new_codes = {}
    for i, code in enumerate(codes):
        new_codes[i] = code
    codes = new_codes

    outputs = []
    r_base = 0 # relative_base
    while True:
        ins = codes[idx]
        if ins == 99:
    	    return outputs, idx, codes

        ins_str = str(ins)
        if len(ins_str) < 5:
            ins_str = '0' * (5 - len(ins_str)) + ins_str
        op = int(ins_str[-2:])

        p_mode = int(ins_str[-3])
        if p_mode == 0:
            num1 = codes.get(codes[idx+1], 0)
        elif p_mode == 1:
            num1 = codes.get(idx+1)
        elif p_mode == 2:
            num1 = codes.get(r_base+codes[idx+1], 0)

        if op == 3: # position mode or relative mode
            if p_mode == 0:
                codes[codes[idx+1]] = input_val
            elif p_mode == 2:
                codes[r_base+codes[idx+1]] = input_val
            idx += 2
            continue

        if op == 4:
            outputs.append(num1)
            idx += 2
            if return_on_output:
                return outputs, idx, codes # immediately return
            continue

        if op == 9: # modified with the relative base offset
            r_base += num1
            idx += 2
            continue

        p_mode = int(ins_str[-4])
        if p_mode == 0:
            num2 = codes.get(codes[idx+2], 0)
        elif p_mode == 1:
            num2 = codes.get(idx+2)
        elif p_mode == 2:
            num2 = codes.get(r_base+codes[idx+2], 0)

        if op in [1, 2]:
            res = num1 + num2 if op == 1 else num1 * num2
            p_mode = int(ins_str[-5])
            if p_mode == 0:
                codes[codes[idx+3]] = res
            elif p_mode == 2:
                codes[r_base+codes[idx+3]] = res
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

        p_mode = int(ins_str[-5])
        if op == 7: # less than
            val = 1 if num1 < num2 else 0
            if p_mode == 0:
                codes[codes[idx+3]] = val
            elif p_mode == 2:
                codes[r_base+codes[idx+3]] = val
            idx += 4
            continue
        if op == 8: # equal
            val = 1 if num1 == num2 else 0
            if p_mode == 0:
                codes[codes[idx+3]] = val
            elif p_mode == 2:
                codes[r_base+codes[idx+3]] = val
            idx += 4
            continue

    return outputs

def part1(codes):
    input_val = 1
    res, _, _ = day5(codes, input_val)
    return res

def part2(codes):
    input_val = 2
    res, _, _ = day5(codes, input_val)
    return res

if __name__ == '__main__':
    # run("input_test1")
    # run("input_test2")
    # run("input_test3")
    run("input")

