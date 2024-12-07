lines = [line.strip().split(":") for line in open("../inputs/day07-real.txt")]
eqns = [(int(l[0]), tuple(int(v) for v in l[1].strip().split(" "))) for l in lines]

add = lambda x,y: x+y
mul = lambda x,y: x*y
cat = lambda x,y: int(str(x) + str(y))

def solvable(ans, vs, ops):
    def solve(vs):
        if len(vs) == 1:
            return vs[0] == ans

        for op in ops:
            nvs = (op(vs[0], vs[1]),) + vs[2:]
            if solve(nvs): return True

        return False

    return solve(vs)

p1 = sum(ans for ans,vs in eqns if solvable(ans, vs, [add, mul]))
p2 = sum(ans for ans,vs in eqns if solvable(ans, vs, [add, mul, cat]))

print(f"Part 1: {p1}")
print(f"Part 1: {p2}")
