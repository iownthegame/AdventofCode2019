from math import floor 

def run():
    filename = "input"

    with open(filename) as f:
        data = f.readlines()
	print(len(data))

        res = part1(data)
        print('part1 ans: %s' % res)

        res = part2(data)
        print('part2 ans: %s' % res)

def part1(data):
    return sum([floor(int(num) / 3) - 2 for num in data])

def cal(fuel):
    output =  floor(int(fuel) / 3) - 2
    return max(output, 0)

def part2(data):
    res = []
    for num in data:
        total = 0
        fuel = int(num)
        while fuel > 0:
            fuel = cal(fuel)
            total += fuel
        res.append(total)
    return sum(res)


if __name__ == '__main__':
    run()

