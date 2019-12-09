import collections

def run():
    start = 347312
    end = 805915

    res = part1(start, end)
    print('part1 ans: %s' % res)

    res = part2(start, end)
    print('part2 ans: %s' % res)

def part1(start, end):
    cnt = 0
    for num in range(start, end+1):
        string = str(num)
        nums = [int(s) for s in string]
        counter = collections.Counter(string)
        if not any([val > 1 for val in counter.values()]):
            continue
        diff = [x - y for x, y in zip(nums[1:], nums)]
        if any([d < 0 for d in diff]):
            continue
        cnt += 1
    return cnt

def part2(start, end):
    cnt = 0
    for num in range(start, end+1):
        string = str(num)
        nums = [int(s) for s in string]
        counter = collections.Counter(string)
        if not any([val > 1 for val in counter.values()]):
            continue
        diff = [x - y for x, y in zip(nums[1:], nums)]
        if any([d < 0 for d in diff]):
            continue
        # the two adjacent matching digits are not part of a larger group of matching digits.
        min_dup_val = float('inf')
        for _key, val in counter.items():
            if val > 1:
                min_dup_val = min(min_dup_val, val)
        if min_dup_val != 2:
            continue
        cnt += 1
    return cnt

if __name__ == '__main__':
    run()

