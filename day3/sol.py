def run(filename, alarm=False):
    print('run file %s' % filename)
    with open(filename) as f:
        data = f.readlines()

        res = part1(data)
        print('part1 ans: %s' % res)

        res = part2(data)
        print('part2 ans: %s' % res)

def detect_dir(line_starts, line_ends):
    if line_starts[0] == line_ends[0]:
        line_dir = 'v'
    else:
        line_dir = 'h'
    return line_dir


def intersects(current_line, lines, steps=[]):
    current_line_starts = current_line[0]
    current_line_ends = current_line[1]
    current_line_dir = detect_dir(current_line_starts, current_line_ends)
    # print('current_line', current_line, current_line_dir)
    res = []
    for line_idx, line in enumerate(lines):
        line_starts = line[0]
        line_ends = line[1]
        line_dir = detect_dir(line_starts, line_ends)
        prev_step = steps[line_idx - 1] if line_idx > 0 else 0
        prev_line_ends = lines[line_idx - 1][1] if line_idx > 0 else [0, 0]
        # print('line', line, line_dir)
        if current_line_dir == line_dir: # same direction
            if line_dir == 'v':
                if line_starts[0] == current_line_starts[0]:
                    # same line
                    line_range = sorted([line_starts[1], line_ends[1]])
		    current_line_range = sorted([current_line_starts[1], current_line_ends[1]])
	            new_range = [max(line_range[0], current_line_range[0]), min(line_range[1], current_line_range[1])]
                    if new_range[1] >= new_range[0]:
                        for i in range(new_range[0], new_range[1]+1):
                            new_point = [line_starts[0], i]
                            need_step = prev_step + dis(new_point, prev_line_ends)
                            res.append([new_point, need_step])
            else:
                if line_starts[1] == current_line_starts[1]:
                    # same line
                    line_range = sorted([line_starts[0], line_ends[0]])
		    current_line_range = sorted([current_line_starts[0], current_line_ends[0]])
	            new_range = [max(line_range[0], current_line_range[0]), min(line_range[1], current_line_range[1])]
                    if new_range[1] >= new_range[0]:
                        for i in range(new_range[0], new_range[1]+1):
                            new_point = [i, line_starts[1]]
                            need_step = prev_step + dis(new_point, prev_line_ends)
                            res.append([new_point, need_step])
        else: # different direction, at most one intersection
            if line_dir == 'v':
                line_range = sorted([line_starts[1], line_ends[1]])
                if line_range[0] <= current_line_starts[1] <= line_range[1]:
                    current_line_range = sorted([current_line_starts[0], current_line_ends[0]])
                    if current_line_range[0] <= line_starts[0] <= current_line_range[1]:
                        new_point = [line_starts[0], current_line_starts[1]]
                        need_step = prev_step + dis(new_point, prev_line_ends)
                        res.append([new_point, need_step])
            else:
                line_range = sorted([line_starts[0], line_ends[0]])
                if line_range[0] <= current_line_starts[0] <= line_range[1]:
                    current_line_range = sorted([current_line_starts[1], current_line_ends[1]])
                    if current_line_range[0] <= line_starts[1] <= current_line_range[1]:
                        new_point = [current_line_starts[0], line_starts[1]]
                        need_step = prev_step + dis(new_point, prev_line_ends)
                        res.append([new_point, need_step])
    # print('intersections', res) 
    return res

def dis(point, point2=[0, 0]):
    if point[0] == 0 and point[1] == 0:
        return float('inf')
    return abs(point[0] - point2[0]) + abs(point[1] - point2[1])

def part1(data):
    first = data[0].split(',')
    second = data[1].split(',')
    start_x = 0
    start_y = 0
    lines = []
    steps = []
    current_steps = 0
    
    for item in first:
        d = item[0]
        num = int(item[1:])
        if d == 'R':
            lines.append([[start_x, start_y], [start_x + num, start_y]])
            start_x += num
        elif d == 'L':
            lines.append([[start_x, start_y], [start_x - num, start_y]])
            start_x -= num
        elif d == 'U':
            lines.append([[start_x, start_y], [start_x, start_y + num]])
            start_y += num
        elif d == 'D':
            lines.append([[start_x, start_y], [start_x, start_y - num]])
            start_y -= num
        current_steps += num
        steps.append(current_steps)
        
    start_x = 0
    start_y = 0
    min_dis = float('inf')
    for item in second:
        d = item[0]
        num = int(item[1:])
        if d == 'R':
            tmp = intersects([[start_x, start_y], [start_x + num, start_y]], lines, steps)
            for new_point, step in tmp:
                min_dis = min(dis(new_point), min_dis)
                # print(new_point, min_dis)
            start_x += num
        elif d == 'L':
            tmp = intersects([[start_x, start_y], [start_x - num, start_y]], lines, steps)
            for new_point, step in tmp:
                min_dis = min(dis(new_point), min_dis)
                # print(new_point, min_dis)
            start_x -= num
        elif d == 'U':
            tmp = intersects([[start_x, start_y], [start_x, start_y + num]], lines, steps)
            for new_point, step in tmp:
                min_dis = min(dis(new_point), min_dis)
                # print(new_point, min_dis)
            start_y += num
        elif d == 'D':
            tmp = intersects([[start_x, start_y], [start_x, start_y - num]], lines, steps)
            for new_point, step in tmp:
                min_dis = min(dis(new_point), min_dis)
                # print(new_point, min_dis)
            start_y -= num
    return min_dis

def part2(data):
    first = data[0].split(',')
    second = data[1].split(',')
    start_x = 0
    start_y = 0
    lines = []
    steps = []
    current_steps = 0
 
    for item in first:
        d = item[0]
        num = int(item[1:])
        if d == 'R':
            lines.append([[start_x, start_y], [start_x + num, start_y]])
            start_x += num
        elif d == 'L':
            lines.append([[start_x, start_y], [start_x - num, start_y]])
            start_x -= num
        elif d == 'U':
            lines.append([[start_x, start_y], [start_x, start_y + num]])
            start_y += num
        elif d == 'D':
            lines.append([[start_x, start_y], [start_x, start_y - num]])
            start_y -= num
        current_steps += num
        steps.append(current_steps)
        
    start_x = 0
    start_y = 0
    min_dis = float('inf')
    current_steps = 0
    last_line_ends = [0, 0]
    for item in second:
        d = item[0]
        num = int(item[1:])
        if d == 'R':
            tmp = intersects([[start_x, start_y], [start_x + num, start_y]], lines, steps)
            for new_point, step in tmp:
                step2 = current_steps + dis(new_point, last_line_ends)
                min_dis = min(step + step2, min_dis)
                # print(new_point, min_dis)
            start_x += num
        elif d == 'L':
            tmp = intersects([[start_x, start_y], [start_x - num, start_y]], lines, steps)
            for new_point, step in tmp:
                step2 = current_steps + dis(new_point, last_line_ends)
                min_dis = min(step + step2, min_dis)
                # print(new_point, min_dis)
            start_x -= num
        elif d == 'U':
            tmp = intersects([[start_x, start_y], [start_x, start_y + num]], lines, steps)
            for new_point, step in tmp:
                step2 = current_steps + dis(new_point, last_line_ends)
                min_dis = min(step + step2, min_dis)
                # print(new_point, min_dis)
            start_y += num
        elif d == 'D':
            tmp = intersects([[start_x, start_y], [start_x, start_y - num]], lines, steps)
            for new_point, step in tmp:
                step2 = current_steps + dis(new_point, last_line_ends)
                min_dis = min(step + step2, min_dis)
                # print(new_point, min_dis)
            start_y -= num
        current_steps += num
        last_line_ends = [start_x, start_y]
    return min_dis

if __name__ == '__main__':
    run("input_test")
    run("input_test1")
    run("input_test2")
    run("input")

