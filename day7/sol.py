def run(filename):
    print('run file %s' % filename)
    with open(filename) as f:
        data = f.readlines()
        data = data[0].replace('\n', '')
        codes = data.split(',')
        codes = list(map(int, codes))

        # print(codes)
        # res = part1(codes)
        # print('part1 ans: %s' % res)

        original_codes = codes[:]
        res = part2(original_codes)
        print('part2 ans: %s' % res)

def day5(codes, input_vals, idx = 0, return_on_output=False):
    outputs = []
    while idx < len(codes):
        # print('idx', idx)
        ins = codes[idx]
        if ins == 99:
    	    return outputs, idx, codes

        ins_str = str(ins)
        if len(ins_str) < 5:
            ins_str = '0' * (5 - len(ins_str)) + ins_str
        op = int(ins_str[-2:])
        if op == 3:
            codes[codes[idx+1]] = input_vals.pop(0)
            idx += 2
            continue
        if op == 4:
            if int(ins_str[-3]) == 0:
                outputs.append(codes[codes[idx+1]])
            else:
                outputs.append(codes[idx+1])
            idx += 2
            if return_on_output:
                return outputs, idx, codes # immediately return
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

def backtrack(idx, path, candidates, lenth_num, output):
    if idx == lenth_num:
        output.append(path)
        return
    for i, num in enumerate(candidates):
        # remove candidates[i]
        backtrack(idx + 1, path + [num], candidates[:i] + candidates[i+1:], lenth_num, output)

def part1(codes):
    # try every phase settings for 5 amplifiers
    permutations = []
    backtrack(0, [], [0, 1, 2, 3, 4], 5, permutations)
    max_thruster = float('-inf')
    for phase in permutations:
        prev_output = 0
        for i in range(5): # amplifiers
            original_codes = codes[:]
            res, _, _ = day5(original_codes, [phase[i], prev_output])
            prev_output = res[0]
        max_thruster = max(max_thruster, prev_output)

    return max_thruster

def part2(codes):
    # try every phase settings for 5 amplifiers
    permutations = []
    len_perm = 5
    backtrack(0, [], [5, 6, 7, 8, 9], len_perm, permutations)
    max_thruster = float('-inf')
    for phase in permutations:
        # prepare data for each amplifiers
        prev_output = 0
        input_vals = [[p] for p in phase]
        input_vals[0].append(0)
        start_indices = [0] * len_perm
        arrays = [codes[:]] * len_perm

        done = False
        while not done: # amplifiers
            # feedback loop
            for amp_i in range(len_perm):
                res, new_index, new_array = day5(arrays[amp_i], input_vals[amp_i], start_indices[amp_i], True)
                if not res:
                    done = True
                    break
                prev_output = res[0]
                start_indices[amp_i] = new_index
                arrays[amp_i] = new_array[:]
                next_amp_i = (amp_i + 1) % len_perm
                input_vals[next_amp_i].append(prev_output)
        max_thruster = max(max_thruster, prev_output)

    return max_thruster


if __name__ == '__main__':
    # run("input_test1")
    # run("input_test2")
    # run("input_test3")
    run("input_test_p2_1")
    run("input_test_p2_2")
    run("input")

