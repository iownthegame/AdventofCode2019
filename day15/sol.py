from copy import deepcopy

def run(filename):
    print('run file %s' % filename)
    with open(filename) as f:
        data = f.readlines()
        data = data[0].replace('\n', '')
        codes = data.split(',')
        codes = list(map(int, codes))

        # change codes array to dictionary
        new_codes = {}
        for i, code in enumerate(codes):
            new_codes[i] = code
        codes = new_codes

        original_codes = deepcopy(codes)

        # print(codes)
        res = part1(codes)
        print('part1 ans: %s' % res)

        res = part2(original_codes)
        print('part2 ans: %s' % res)

def day5(codes, input_val, idx=0, r_base = 0, return_on_output=False):
    """
    The computer's available memory should be much larger than the initial program. Memory beyond the initial program starts with the value 0 and can be read or written like any other memory.
    """
    outputs = []
    while True:
        ins = codes[idx]
        if ins == 99:
    	    return outputs, idx, r_base, codes

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
                return outputs, idx, r_base, codes # immediately return
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

NORTH, SOUTH, WEST, EAST = [i for i in range(1, 5)]
WALL, MOVED, OXYGEN = [i for i in range(3)]

def get_new_pos(current_pos, direction):
    x, y = current_pos
    if direction == NORTH:
        return (x - 1, y)
    if direction == SOUTH:
        return (x + 1, y)
    if direction == EAST:
        return (x, y - 1)
    if direction == WEST:
        return (x, y + 1)

def part1(codes):
    pos = (0, 0)

    r_base = 0
    idx = 0
    original_codes = deepcopy(codes)
    steps = 0
    queue = [[pos, idx, r_base, original_codes, steps]]

    visited = set()
    found = None
    min_steps = None

    # run until find first oxygen, bfs
    while not found:
        current_pos, current_idx, current_r_base, current_codes, steps = queue.pop(0)
        visited.add(current_pos)
        # print('visit current_pos', current_pos)
        steps += 1
        for i in range(1, 5):
            input_val = i
            direction = i
            new_pos = get_new_pos(current_pos, direction)
            if new_pos in visited:
                continue
            run_codes = deepcopy(current_codes)
            res, new_idx, new_r_base, new_codes = day5(run_codes, input_val, current_idx, current_r_base, return_on_output=True)
            output = res[0]
            # print('new_pos', new_pos, 'output', output)
            if output == WALL:
                continue
            if output == MOVED:
                new_codes = deepcopy(new_codes)
                queue.append([new_pos, new_idx, new_r_base, new_codes, steps])
                continue
            if output == OXYGEN:
                found = new_pos
                min_steps = steps
                break

    print('found oxygen', found)
    return min_steps

def part2(codes):
    graph = {}
    pos = (0, 0)
    graph['0,0'] = 1

    r_base = 0
    idx = 0
    original_codes = deepcopy(codes)
    steps = 0
    queue = [[pos, idx, r_base, original_codes, steps]]

    visited = set()
    # found = None
    # min_steps = None

    # run until finish graph
    while queue:
        current_pos, current_idx, current_r_base, current_codes, steps = queue.pop(0)
        # print('visit current_pos', current_pos)
        if current_pos in visited:
            continue
        visited.add(current_pos)
        steps += 1
        for i in range(1, 5):
            input_val = i
            direction = i
            new_pos = get_new_pos(current_pos, direction)
            new_pos_key = f"{new_pos[0]},{new_pos[1]}"
            run_codes = deepcopy(current_codes)
            res, new_idx, new_r_base, new_codes = day5(run_codes, input_val, current_idx, current_r_base, return_on_output=True)
            output = res[0]
            # print('new_pos', new_pos, 'output', output)
            graph[new_pos_key] = output
            if output == WALL:
                visited.add(new_pos)
                continue
            if output == MOVED:
                new_codes = deepcopy(new_codes)
                queue.append([new_pos, new_idx, new_r_base, new_codes, steps])
                continue
            if output == OXYGEN:
                new_codes = deepcopy(new_codes)
                queue.append([new_pos, new_idx, new_r_base, new_codes, steps])
                # found = new_pos
                # min_steps = steps
                continue

    print('finished walking')

    # make graph
    Xs = []
    Ys = []

    for key in graph:
        x, y = key.split(',')
        Xs.append(int(x))
        Ys.append(int(y))

    min_x = min(Xs)
    max_x = max(Xs)
    min_y = min(Ys)
    max_y = max(Ys)

    print('x', min_x, max_x)
    print('y', min_y, max_y)

    len_x = max_x - min_x + 1
    len_y = max_y - min_y + 1
    print('len', len_x, len_y)

    grid = [[' '] * len_y for _ in range(len_x)]
    paint = ['#', '.', 'O']
    for key in graph:
        x, y = key.split(',')
        val = graph[key]
        pos_x = int(x) - min_x
        pos_y = int(y) - min_y

        grid[pos_x][pos_y] = paint[val]
        if val == 2:
            oxy = (pos_x, pos_y)
            print('oxygen:', pos_x, pos_y)

    for line in grid:
        print(''.join(line))

    # calculate oxygen spread minutes
    minutes = -1
    queue = [oxy]
    visited = set()

    # bfs
    while queue:
        new_queue = []
        for pos in queue:
            if pos in visited:
                continue
            visited.add(pos)
            for x, y in [[0, 1], [0, -1], [-1, 0], [1, 0]]:
                new_x = pos[0] + x
                new_y = pos[1] + y
                if 0 <= new_x < len_x and 0 <= new_y < len_y and grid[new_x][new_y] == '.':
                    grid[new_x][new_y] = 'O'
                    new_queue.append((new_x, new_y))
        queue = new_queue
        minutes += 1
        # print('spreading at minute', minutes, queue)

    # for line in grid:
    #     print(''.join(line))

    return minutes

if __name__ == '__main__':
    run("input")

