
from heapq import heappush, heappop
def run(filename):
    print('run file %s' % filename)
    with open(filename) as f:
        data = f.readlines()
        asteroids = []
        y = 0
        for line in data:
            line = line.strip()
            x = 0
            for c in line:
                if c == '#':
                    asteroids.append([x, y])
                x += 1
            y += 1
        # print(asteroids)

        res = part1(asteroids)
        print('part1 ans: %s %s' % (res[0], res[1]))

        res = part2(asteroids, res[1])
        print('part2 ans: %s' % res)

def part1(asteroids):
    max_num = float('-inf')
    max_num_pos = None
    table = {}

    for a in asteroids:
        slopes = set()
        # print('asteroid:', a)
        for b in asteroids:
            if b != a:
                if b[1] == a[1]: # horizontal
                    if b[0] > a[0]:
                        slope = 'h+1'
                    else:
                        slope = 'h-1'
                elif b[0] == a[0]: # vertical
                    if b[1] > a[1]:
                        slope = 'v+1'
                    else:
                        slope = 'v-1'
                else:
                    slope = float(1.0 * (b[1] - a[1]) / (b[0] - a[0]))
                    slope_str = str(slope)
                    if b[1] > a[1]:
                        slope = slope_str + 'a'
                    else:
                        slope = slope_str + 'b'
                # print(b, slope)
                slopes.add(slope)

        current_num = len(slopes)
        # print('asteroid:', a, 'num: ', current_num)

        key = '%s-%s' % (a[0], a[1])
        table[key] = current_num

        if current_num > max_num:
            max_num = current_num
            max_num_pos = a

    # print(table)
    return max_num, max_num_pos

def part2(asteroids, pos):
    table_u = []
    table_ur = {}
    table_r = []
    table_dr = {}
    table_d = []
    table_dl = {}
    table_l = []
    table_ul = {}

    a = pos
    asteroids.remove(pos)
    for b in asteroids:
        if b[1] == a[1]: # horizontal
            if b[0] > a[0]:
                table = table_r
            else:
                table = table_l
            dis = abs(b[0] - a[0])
            heappush(table, (dis, b))
        elif b[0] == a[0]: # vertical
            if b[1] < a[1]:
                table = table_u
            else:
                table = table_d
            dis = abs(b[1] - a[1])
            heappush(table, (dis, b))
        else:
            slope = float(1.0 * (b[1] - a[1]) / (b[0] - a[0]))
            # slope_str = str(slope)
            dis = abs(b[1] - a[1]) + abs(b[0] - a[0])
            if slope > 0:
                if b[1] > a[1]:
                    table = table_dr
                else:
                    table = table_ul
            elif slope < 0:
                if b[1] < a[1]:
                    table = table_ur
                else:
                    table = table_dl
            slope *= -1
            if not slope in table:
                table[slope] = []
            heappush(table[slope], (dis, b))

    # # clockwise
    class Table:
        def __init__(self, table, order, attribute):
            self.table = table
            self.order = order
            self.attribute = attribute

    table_dirs = [
        Table(table_u, 'line', 'u'),
        Table(table_ur, 'desc', 'ur'),
        Table(table_r, 'line', 'r'),
        Table(table_dr, 'desc', 'dr'),
        Table(table_d, 'line', 'd'),
        Table(table_dl, 'desc', 'dl'),
        Table(table_l, 'line', 'l'),
        Table(table_ul, 'desc', 'ul'),
    ]

    labels = []
    while asteroids:
        for t in table_dirs:
            table = t.table
            order = t.order
            if order == 'line':
                if not table:
                    continue
                dis, pos = heappop(table)
                labels.append(pos)
                asteroids.remove(pos)
            else:
                keys = list(table.keys())
                if not keys:
                    continue
                reverse = True if order == 'desc'else False
                keys.sort(reverse=reverse)
                for key in keys:
                    if table[key]:
                        dis, pos = heappop(table[key])
                        labels.append(pos)
                        asteroids.remove(pos)
                        if not table[key]:
                            del table[key]
    # print(len(labels))
    # print(labels)
    return labels[199]

if __name__ == '__main__':
    # run("input_test1")
    # run("input_test2")
    # run("input_test3")
    # run("input_test4")
    # run("input_test5")
    # run("input_test_p2")
    run("input")

