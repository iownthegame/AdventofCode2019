from collections import defaultdict
import math
from copy import deepcopy

def run(filename):
    print('run file %s' % filename)
    with open(filename) as f:
        data = f.readlines()
        table, bases = preprocess(data)

        original_table = deepcopy(table)
        res = part1(table, bases)
        print('part1 ans: %s' % res)

        res = part2(original_table, bases)
        print('part2 ans: %s' % res)

def get_ingredient(source):
    num, ingredient = source.split(' ')
    return int(num), ingredient

def preprocess(data):
    table = {}
    bases = []
    for d in data:
        sources, result = d.strip().split(' => ')
        result_num, result_ingredient = get_ingredient(result)
        table[result_ingredient] = {'unit': result_num, 'ingredients': {}}

        if 'ORE' in sources:
            bases.append(result_ingredient)

        tmp = sources.split(', ')
        for source in tmp:
            num, ingredient = get_ingredient(source)
            table[result_ingredient]['ingredients'].update({ingredient: num})
    return table, bases

def part1(original_table, bases, fuel_amount=1):
    """generate 1 FUEL"""

    table = deepcopy(original_table)
    cal_table = table['FUEL']['ingredients']
    for key in cal_table:
        cal_table[key] *= fuel_amount
    del table['FUEL']

    # bfs
    while True:
        # print('in loop')
        # print('cal table', cal_table)
        new_cal_table = defaultdict(int)

        # get targets ===> not ingredients by other chemicals
        targets = list(table.keys())
        for key in table:
            ingredients = table[key]['ingredients']
            for ing in ingredients:
                if ing in targets:
                    targets.remove(ing)
        # print('targets', targets)

        for current_ing, current_unit in cal_table.items():
            if not current_ing in targets:
                # print('keep', current_ing)
                new_cal_table[current_ing] += current_unit
                continue

            # replace chemicals !!!
            # print('replace', current_ing)
            need = table[current_ing]
            ingredients = need['ingredients']
            times = int(math.ceil(1.0 * current_unit / need['unit']))
            for ing, num in ingredients.items():
                new_cal_table[ing] += num * times
            del table[current_ing]

        cal_table = deepcopy(new_cal_table)

        if len(cal_table.keys()) == 1 and 'ORE' in cal_table:
            break

    return cal_table['ORE']

def part2(table, bases):
    # binary search
    total_ore = 1000000000000
    ore_for_a_fuel = part1(table, bases, fuel_amount=1)
    left = 1
    right = total_ore // ore_for_a_fuel * 2
    max_ore = float('-inf')
    max_fuel = 1
    while left <= right:
        mid = (left + right) // 2
        current_ore = part1(table, bases, fuel_amount=mid)
        if current_ore == total_ore:
            return mid
        if current_ore > total_ore:
            right = mid - 1
        else:
            left = mid + 1
        if current_ore < total_ore and current_ore > max_ore:
            max_ore = current_ore
            max_fuel = mid

    return max_fuel

if __name__ == '__main__':
    # run("input_test_1")
    # run("input_test_2")
    # run("input_test_3")
    # run("input_test_4")
    # run("input_test_5")
    run("input")

