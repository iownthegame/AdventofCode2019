import threading

def run(filename, phases):
    print('run file %s' % filename)
    with open(filename) as f:
        data = f.readlines()
        data = data[0].replace('\n', '')
        codes = data
        codes = list(map(int, codes))

        original_codes = codes[:]
        # print(codes)

        # res = part1(codes, phases)
        # print('part1 ans: %s' % ''.join(map(str, res[:8])))

        res = part2(original_codes, phases)
        print('part2 ans: %s' % ''.join(map(str, res[:8])))

def generate_bases(repeat):
    BASE = [0, 1, 0, -1]
    current_base = [b for b in BASE for _ in range(repeat)]
    current_base.append(current_base.pop(0)) # shift 1
    return current_base

# def generate_bases(length, repeat):
#     BASE = [0, 1, 0, -1]
#     bases = []
#     idx = 0
#     b_idx = 0
#     while idx < length + 1:
#         bases += [BASE[b_idx]] * repeat
#         b_idx = (b_idx + 1 ) % len(BASE)
#         idx += repeat
#     bases = bases[1: length + 1] # shift
#     return bases

def async_cal(t_idx, threads_num, codes, new_codes, length):
    # print('thread', t_idx, 'calculating...')
    idx_range = length // threads_num
    # print(idx_range)
    start_idx = t_idx * idx_range
    # print('start idx', start_idx)

    for i in range(start_idx, start_idx + idx_range):
        # bases = generate_bases(length, i + 1)
        current_base = generate_bases(i + 1)
        # print(current_base)
        len_base = 4 * (i + 1)
        total = abs(sum([(codes[c] * current_base[c % len_base]) for c in range(length)])) % 10
        new_codes[i] = total
        # print('total for idx %s is %s' % (i, total))
    # print('thread', t_idx, 'finished...')

def calculate(codes):
    length = len(codes)
    new_codes = [0] * length
    threads = []

    threads_num = 1
    for t in range(threads_num):
        copy_codes = codes[:]
        thread = threading.Thread(target=async_cal, args=(t, threads_num, copy_codes, new_codes, length))
        thread.daemon = True
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return new_codes

def part1(codes, phases):
    for _ in range(phases):
        codes = calculate(codes)
        # print('codes', codes)
    return codes

# multiple processing doesn't work, still run too slow....
# def part2(codes, phases):
#     phases = 1
#     offset = int(''.join(map(str, codes[:7])))
#     print('offset', offset)
#     print('codes', len(codes))
#     base_codes = codes[:]
#     for _ in range(9999):
#         codes += base_codes
#     print('concated codes', len(codes))
#     for _ in range(phases):
#         codes = calculate(codes)
#         # print('codes', codes)
#     return codes[offset:]

def part2(codes, phases):
    """
    from the example below, we founnd:
    1. the second-half of the signal is just the sum of each digit after current digit
        8 => 8
        5 => 8 + 7
        1 => 8 + 7 + 6
        6 => 8 + 7 + 6 + 5

    Input signal: 12345678
    1*1  + 2*0  + 3*-1 + 4*0  + 5*1  + 6*0  + 7*-1 + 8*0  = 4
    1*0  + 2*1  + 3*1  + 4*0  + 5*0  + 6*-1 + 7*-1 + 8*0  = 8
    1*0  + 2*0  + 3*1  + 4*1  + 5*1  + 6*0  + 7*0  + 8*0  = 2
    1*0  + 2*0  + 3*0  + 4*1  + 5*1  + 6*1  + 7*1  + 8*0  = 2
    1*0  + 2*0  + 3*0  + 4*0  + 5*1  + 6*1  + 7*1  + 8*1  = 6
    1*0  + 2*0  + 3*0  + 4*0  + 5*0  + 6*1  + 7*1  + 8*1  = 1
    1*0  + 2*0  + 3*0  + 4*0  + 5*0  + 6*0  + 7*1  + 8*1  = 5
    1*0  + 2*0  + 3*0  + 4*0  + 5*0  + 6*0  + 7*0  + 8*1  = 8

    further foundings:
    the offset giving in part2 are all at second-half parts of signal
    so we could just shift with the offset and do the sum of each digit from end to begin
    """

    offset = int(''.join(map(str, codes[:7])))
    base_codes = codes[:]
    for _ in range(9999):
        codes += base_codes
    codes = codes[offset:]

    for _ in range(phases):
        new_codes = [0] * len(codes)
        total = 0
        for i in range(len(codes) - 1, -1, -1):
            total += codes[i]
            new_codes[i] = abs(total) % 10
        codes = new_codes
    return codes

if __name__ == '__main__':
    # run("input_test_1", phases=4)
    # run("input_test_2", phases=100)
    # run("input_test_3", phases=100)
    # run("input_test_4", phases=100)
    run("input_test_p2_1", phases=100)
    run("input_test_p2_2", phases=100)
    run("input_test_p2_3", phases=100)
    run("input", phases=100)
