def run(filename, alarm=False):
    print('run file %s' % filename)
    with open(filename) as f:
        data = f.readlines()

        # res = part1(data)
        # print('part1 ans: %s' % res)

        start = 'YOU'
        end = 'SAN'
        res = part2(data, start, end)
        print('part2 ans: %s' % res)

def part1(data):
    table = {}
    count_table = {}
    for d in data:
        src, dst = d.strip().split(')') # COM)B
        table[dst] = src
    # print(table)

    for key in table:
        count_table[key] = 1
        src = table[key]
        while src in table:
            count_table[key] += 1
            if src == 'COM':
                break
            src = table[src]

    return sum(count_table.values())

def get_orbits(src, table):
    res = []
    while src in table:
        res.append(src)
        if src == 'COM':
            break
        src = table[src]
    return res

def part2(data, start, end):
    table = {}
    for d in data:
        src, dst = d.strip().split(')') # COM)B
        table[dst] = src
    # print(table)

    start_orbits = get_orbits(table[start], table)
    end_orbits = get_orbits(table[end], table)

    # print(start_orbits)
    # print(end_orbits)
    # find first match in orbits
    intersects = list(set(start_orbits) & set(end_orbits))
    min_orbits = float('inf')
    for match in intersects:
        orbits = (start_orbits.index(match)) + (end_orbits.index(match))
        # print(match, orbits)
        min_orbits = min(min_orbits, orbits)
    return min_orbits

if __name__ == '__main__':
    # run("input_test")
    run("input_test_p2")
    run("input")

