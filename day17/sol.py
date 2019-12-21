def run(filename):
    print('run file %s' % filename)
    with open(filename) as f:
        data = f.readlines()
        data = data[0].replace('\n', '')
        codes = data.split(',')
        codes = list(map(int, codes))
        original_codes = codes[:]

        # print(codes)

        res, graph, start_pos = part1(codes)
        print('part1 ans: %s' % res)

        res = part2(original_codes, graph, start_pos)
        print('part2 ans: %s' % res)

def day5(codes, input_vals, idx=0, return_on_output=False):
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
                codes[codes[idx+1]] = input_vals.pop(0)
            elif p_mode == 2:
                codes[r_base+codes[idx+1]] = input_vals.pop(0)
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
    input_vals = []
    res, _, _ = day5(codes, input_vals)
    graph = []
    line = []
    start_pos = (0, 0)
    row = 0
    for c in res:
        if c == 35: # scaffold
            line.append('#')
        elif c == 46: # open space
            line.append('.')
        elif c == 10: # new line
            if line:
                graph.append(line)
                line = []
                row += 1
        else: # ^
            line.append(chr(c))
            start_pos = (row, len(line) - 1)

    for line in graph:
        print (''.join(line))

    M = len(graph)
    N = len(graph[0])
    dirs = [[0, 0], [0, 1], [0, -1], [-1, 0], [1, 0]]
    intersections = []
    # print('M', M, 'N', N)
    for i in range(1, M-1):
        for j in range(1, N-1):
            if all([graph[i + di][j + dj] == '#' for di, dj in dirs]):
                intersections.append([i, j])
    return sum([x * y for x, y in intersections]), graph, start_pos

def generate_path(graph, start_pos):
    M = len(graph)
    N = len(graph[0])
    pos = start_pos
    current_dir = 'U'
    move = 0
    path = []
    dirs = { # try directions: move forward -> turn left / turn right
        'U': [(-1, 0), (0, -1), (0, 1)],
        'L': [(0, -1), (1, 0), (-1, 0)],
        'R': [(0, 1), (-1, 0), (1, 0)],
        'D': [(1, 0), (0, 1), (0, -1)],
    }
    while True:
        i, j = pos
        forward = False
        dir_order = dirs[current_dir]
        for x, y in dir_order:
            new_i, new_j = i + x, j + y
            if 0 <= new_i < M and 0 <= new_j < N and graph[new_i][new_j] == '#':
                forward = True
                if current_dir == 'U':
                    if new_i == i:
                        if new_j < j:
                            if move:
                                path.append(move+1)
                                move = 0
                            path.append('L')
                            next_dir = 'L'
                            current_dir = next_dir
                        else:
                            if move:
                                path.append(move+1)
                                move = 0
                            path.append('R')
                            next_dir = 'R'
                            current_dir = next_dir
                    else:
                        # move forward
                        move += 1
                elif current_dir == 'L':
                    if new_j == j:
                        if new_i < i:
                            if move:
                                path.append(move+1)
                                move = 0
                            path.append('R')
                            next_dir = 'U'
                            current_dir = next_dir
                        else:
                            if move:
                                path.append(move+1)
                                move = 0
                            path.append('L')
                            next_dir = 'D'
                            current_dir = next_dir
                    else:
                        # move forward
                        move += 1
                elif current_dir == 'R':
                    if new_j == j:
                        if new_i < i:
                            if move:
                                path.append(move+1)
                                move = 0
                            path.append('L')
                            next_dir = 'U'
                            current_dir = next_dir
                        else:
                            if move:
                                path.append(move+1)
                                move = 0
                            path.append('R')
                            next_dir = 'D'
                            current_dir = next_dir
                    else:
                        # move forward
                        move += 1
                elif current_dir == 'D':
                    if new_i == i:
                        if new_j < j:
                            if move:
                                path.append(move+1)
                                move = 0
                            path.append('R')
                            next_dir = 'L'
                            current_dir = next_dir
                        else:
                            if move:
                                path.append(move+1)
                                move = 0
                            path.append('L')
                            next_dir = 'R'
                            current_dir = next_dir
                    else:
                        # move forward
                        move += 1
                pos = (new_i, new_j)
                break
        if not forward:
            if move:
                path.append(move+1)
            print('pos not forward', pos)
            break
    return path

def generate_input(input_vals, string):
    for s in string:
        input_vals += [ord(s)]

def part2(codes, graph, start_pos):
    print('start_pos', start_pos)

    path = generate_path(graph, start_pos)
    print(path)
    """ get path by hands and eyes
    ['L', 10, 'L', 6, 'R', 10, 'R', 6, 'R', 8, 'R', 8, 'L', 6, 'R', 8, 'L', 10, 'L', 6, 'R', 10, 'L', 10, 'R', 8, 'R', 8, 'L', 10, 'R', 6, 'R', 8, 'R', 8, 'L', 6, 'R', 8, 'L', 10, 'R', 8, 'R', 8, 'L', 10, 'R', 6, 'R', 8, 'R', 8, 'L', 6, 'R', 8, 'L', 10, 'L', 6, 'R', 10, 'L', 10, 'R', 8, 'R', 8, 'L', 10, 'R', 6, 'R', 8, 'R', 8, 'L', 6, 'R', 8]
    A = 'L', 10, 'L', 6, 'R', 10
    B = 'R', 6, 'R', 8, 'R', 8, 'L', 6, 'R', 8
    C = 'L', 10, 'R', 8, 'R', 8, 'L', 10
    => A,B,A,C,B,C,B,A,C,B
    [65, 44, 66, 44, 65, 44, 67, 44, 66, 44, 67, 44, 66, 44, 65, 44, 67, 44, 66, 10]
    """

    main_routine = 'A,B,A,C,B,C,B,A,C,B\n'
    func_A = 'L,10,L,6,R,10\n'
    func_B =  'R,6,R,8,R,8,L,6,R,8\n'
    func_C = 'L,10,R,8,R,8,L,10\n'
    # video = 'y\n'
    video = 'n\n'

    input_vals = []
    generate_input(input_vals, main_routine)
    # print('main_routine')
    # print(main_routine)
    # print(input_vals)
    generate_input(input_vals, func_A)
    # print('func_A')
    # print(func_A)
    # print(input_vals)
    generate_input(input_vals, func_B)
    # print('func_B')
    # print(func_B)
    # print(input_vals)
    generate_input(input_vals, func_C)
    # print('func_C')
    # print(func_C)
    # print(input_vals)
    generate_input(input_vals, video)
    print(input_vals)

    codes[0] = 2

    ### continuous video feed: apply 'y\n' for debugging
    # line = []
    # output = []
    # for c in res:
    #     if c == 35: # scaffold
    #         line.append('#')
    #     elif c == 46: # open space
    #         line.append('.')
    #     elif c == 10: # new line
    #         if line:
    #             output.append(line)
    #             line = []
    #     else: # ^
    #         line.append(chr(c))

    ### when output answer: apply 'n\n'
    res, _, _ = day5(codes, input_vals)
    res = [r for r in res if r > 127 or r < 0]

    return res

if __name__ == '__main__':
    run("input")

