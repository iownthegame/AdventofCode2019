import re, copy

def run(filename, steps):
    print('run file %s' % filename)
    with open(filename) as f:
        data = f.readlines()

        moons = []
        for d in data:
            pos = re.findall(r"[-+]?[0-9]+", d)
            moons.append(Moon(pos))

        original_moons = copy.deepcopy(moons)

        res = part1(moons, steps)
        print('part1 ans: %s' % res)

        res = part2(original_moons)
        print('part2 ans: %s' % res)

class Pos:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def output(self):
        return [self.x, self.y, self.z]

class Velocity:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def output(self):
        return [self.x, self.y, self.z]

class Moon:
    def __init__(self, pos):
        self.pos = Pos(int(pos[0]), int(pos[1]), int(pos[2]))
        self.vel = Velocity(0, 0, 0)

    def equal(self, other, axis):
        if axis == 'x':
            return self.pos.x == other.pos.x and self.vel.x == other.vel.x
        if axis == 'y':
            return self.pos.y == other.pos.y and self.vel.y == other.vel.y
        if axis == 'z':
            return self.pos.z == other.pos.z and self.vel.z == other.vel.z

def energy(moons):
    total = 0
    for moon in moons:
        pot = abs(moon.pos.x) + abs(moon.pos.y) + abs(moon.pos.z)
        kin = abs(moon.vel.x) + abs(moon.vel.y) + abs(moon.vel.z)
        total += pot * kin
    return total

def update_moon_vel(moons, i, j, axis):
    moon_a = moons[i]
    moon_b = moons[j]
    if axis == 'x':
        if moon_b.pos.x > moon_a.pos.x:
            moon_b.vel.x -= 1
            moon_a.vel.x += 1
        elif moon_b.pos.x < moon_a.pos.x:
            moon_b.vel.x += 1
            moon_a.vel.x -= 1
    elif axis == 'y':
        if moon_b.pos.y > moon_a.pos.y:
            moon_b.vel.y -= 1
            moon_a.vel.y += 1
        elif moon_b.pos.y < moon_a.pos.y:
            moon_b.vel.y += 1
            moon_a.vel.y -= 1
    elif axis == 'z':
        if moon_b.pos.z > moon_a.pos.z:
            moon_b.vel.z -= 1
            moon_a.vel.z += 1
        elif moon_b.pos.z < moon_a.pos.z:
            moon_b.vel.z += 1
            moon_a.vel.z -= 1

def update_moon_pos(moons, i, axis):
    moon = moons[i]
    if axis == 'x':
        moon.pos.x += moon.vel.x
    elif axis == 'y':
        moon.pos.y += moon.vel.y
    elif axis == 'z':
        moon.pos.z += moon.vel.z

def part1(moons, steps):
    M = len(moons)
    for _ in range(steps):
        # update velocity by gravity
        for i in range(M):
            for j in range(i+1, M):
                update_moon_vel(moons, i, j, 'x')
                update_moon_vel(moons, i, j, 'y')
                update_moon_vel(moons, i, j, 'z')

        # update position by velocity
        for i in range(M):
            update_moon_pos(moons, i, 'x')
            update_moon_pos(moons, i, 'y')
            update_moon_pos(moons, i, 'z')

    return energy(moons)

def count_step(moons, axis):
    static_moons = copy.deepcopy(moons)
    steps = 0
    M = len(moons)

    while True:
        # update velocity by gravity
        for i in range(M):
            for j in range(i+1, M):
                update_moon_vel(moons, i, j, axis)

        # update position by velocity
        for i in range(M):
            update_moon_pos(moons, i, axis)

        steps += 1

        if all([moons[i].equal(static_moons[i], axis) for i in range(M)]):
            break

    return steps

def find_lcm(num1, num2):
    if num1 > num2:
        num = num1
        den = num2
    else:
        num = num2
        den = num1
    rem = num % den
    while rem != 0 :
        num = den
        den = rem
        rem = num % den
    gcd = den
    lcm = int(int(num1 * num2)/int(gcd))
    return lcm

def part2(moons):
    steps = 0
    originals = {'x': copy.deepcopy(moons), 'y': copy.deepcopy(moons), 'z': copy.deepcopy(moons)}
    steps = {'x': 0, 'y': 0, 'z': 0}
    for axis in steps:
        steps[axis] = count_step(originals[axis], axis)

    lcm = find_lcm(steps['x'], steps['y'])
    lcm = find_lcm(lcm, steps['z'])
    return lcm

if __name__ == '__main__':
    # run("input_test_1", 10)
    # run("input_test_2", 100)
    run("input", 1000)

