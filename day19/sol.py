def run(filename):
    print('run file %s' % filename)
    with open(filename) as f:
        data = f.readlines()
        data = data[0].replace('\n', '')
        codes = data.split(',')
        codes = list(map(int, codes))

        res = part1(codes)
        print('part1 ans: %s' % res)

        # res = part2(codes)
        # print('part2 ans: %s' % res)

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

def generate_beam(M, codes):
    output = [[-1] * M for _ in range(M)]
    for i in range(M):
        for j in range(M):
            res, _, _ = day5(codes, input_vals=[j, i], return_on_output=True)
            output[j][i] = res[0]
    return output

def part1(codes):
    output = generate_beam(50, codes)
    res = sum(map(sum, output))
    return res

# def part2(codes): # find a 100x100 square in the beam...
#     M = 100
#     output = generate_beam(M, codes)
#     for i in range(M):
#         for j in range(M):
#             output[i][j] = '#' if output[i][j] else '.'

#     # visulization
#     for i in range(M):
#         print(''.join(output[i]))

#     ## find max square
#     # calculating '#' range in each row and each col
#     row_seg = []
#     for i in range(M):
#         row = output[i]
#         if not '#' in row:
#             row_seg.append([-1, -1])
#             continue
#         start = row.index('#')
#         end = M - 1 - row[::-1].index('#')
#         row_seg.append([start, end])

#     col_seg = []
#     for j in range(M):
#         col =[output[i][j] for i in range(M)]
#         if not '#' in col:
#             col_seg.append([-1, -1])
#             continue
#         start = col.index('#')
#         end = M - 1 - col[::-1].index('#')
#         col_seg.append([start, end])

#     print(row_seg)
#     print(col_seg)

#     # go through every point
#     max_square_length = 1
#     max_square_pos = None

#     for i in range(M): # X is toward right, Y is toward down
#         for j in range(M):
#             if output[i][j] != '#':
#                 continue
#             row_start, row_end = row_seg[i]
#             col_start, col_end = col_seg[j]

#             if row_start <= j <= row_end:
#                 max_row_length = row_end - j + 1
#             else:
#                 continue

#             if col_start <= i <= col_end:
#                 max_col_length = col_end - i + 1
#             else:
#                 continue

#             current_max_length = min(max_row_length, max_col_length)

#             if current_max_length > max_square_length:
#                 max_square_length = current_max_length
#                 max_square_pos = (i, j)
#             # elif current_max_length == max_square_length:
#             #     max_square_pos.append((i, j))

#     print(max_square_length)
#     print(max_square_pos)
#     pos = max_square_pos
#     output[pos[0]][pos[1]] = 'O'
#     # visulization
#     for i in range(M):
#         print(''.join(output[i]))

#     return None
#     # return max_square_pos[0] * 10000 + max_square_pos[1]

if __name__ == '__main__':
    run("input")

