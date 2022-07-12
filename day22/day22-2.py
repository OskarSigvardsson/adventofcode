import re

# a cube is (sign, x1, x2, y1, y2, z1, z2), where the sign indicates if it's a
# negative or positive cube (i.e. it is -1 or 1)

def intersect(c1, c2):
    # intersecting flips the sign
    fs = (lambda _,x:-x, max, min, max, min, max, min)
    c3 = tuple(f(a,b) for (f,a,b) in zip(fs, c1, c2))

    if c3[1] > c3[2] or c3[3] > c3[4] or c3[5] > c3[6]:
        return None

    return c3

with open("input.txt", "r") as f:
    regex = re.compile(R"(on|off) x=(.*)\.\.(.*),y=(.*)\.\.(.*),z=(.*)\.\.(.*)")

    total = []

    for line in f:
        gs = regex.match(line).groups()
        new_cube = (1 if gs[0] == "on" else -1,) + tuple(int(g) for g in gs[1:])

        # the off case is the same as the on case, except we don't add the original cube
        adding = [new_cube] if new_cube[0] == 1 else []

        for cube in total:
            inter = intersect(new_cube, cube)

            if inter:
                adding.append(inter)

        total.extend(adding)
    
    vol = 0

    for c in total:
        vol += c[0] * (c[2] - c[1] + 1) * (c[4] - c[3] + 1) * (c[6] - c[5] + 1)

    print(vol)

