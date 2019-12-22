def run(filename, num_cards):
    print('run file %s' % filename)
    with open(filename) as f:
        data = f.readlines()

        res = part1(data, num_cards)
        if filename == 'input':
            res = res.index(2019)
        print('part1 ans: %s' % res)

        # res = part2(data, num_cards)
        # print('part2 ans: %s' % res)

INS_NEW_STACK, INS_CUT, INS_INCREMENT = 1, 2, 3
def process_instructions(data):
    instructions = []
    for d in data:
        d = d.strip()
        if d == 'deal into new stack':
            instructions.append((INS_NEW_STACK, 0))
        elif 'cut' in d:
            cut_num = int(d.split('cut ')[1])
            instructions.append((INS_CUT, cut_num))
        else:
            increment_num = int(d.split('deal with increment ')[1])
            instructions.append((INS_INCREMENT, increment_num))
    return instructions

def process_cards(cards, ins):
    num_cards = len(cards)
    if ins[0] == INS_NEW_STACK:
        return cards[::-1]
    if ins[0] == INS_CUT:
        cut_num = ins[1]
        if cut_num < 0:
            cut_num += num_cards
        return cards[cut_num:] + cards[:cut_num]
    if ins[0] == INS_INCREMENT:
        new_cards = cards[:]
        increment_num = ins[1]
        idx = 0
        cnt = 0
        while cnt < num_cards:
            new_cards[idx] = cnt
            idx = (idx + increment_num) % num_cards
            cnt += 1
        return [cards[i] for i in new_cards]

def part1(data, num_cards):
    instructions = process_instructions(data)
    cards = [i for i in range(num_cards)]
    for ins, _d in zip(instructions, data):
        cards = process_cards(cards, ins)
        # print(_d.strip())
        # print(cards)
    return cards

# def part2(data, num_cards):
#     instructions = process_instructions(data)
#     cards = [i for i in range(num_cards)]
#     for t in range(200):
#         for ins, _d in zip(instructions, data):
#             cards = process_cards(cards, ins)
#             # print(_d.strip())
#             # print(cards)
#         print(cards[2020])
#     return None

if __name__ == '__main__':
    # run("input_test_1", 10)
    # run("input_test_2", 10)
    # run("input_test_3", 10)
    # run("input_test_4", 10)
    run("input", 10007)
    # run("input", 119315717514047) # part2


