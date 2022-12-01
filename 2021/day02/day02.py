
# part 1
with open("input.txt", "r") as f:
    x,y = 0,0
    dirs = {
        "forward": lambda d: (x + d, y),
        "up"     : lambda d: (x, y - d),
        "down"   : lambda d: (x, y + d),
    }

    for line in f:
        action, d = line.strip().split()
        x,y = dirs[action](int(d))

    print(f"Part 1: {x * y}")

# part 2
with open("input.txt", "r") as f:
    aim,depth,forward = 0,0,0

    dirs = {
        "forward": lambda d: (aim, depth + d * aim, forward + d),
        "up"     : lambda d: (aim - d, depth, forward),
        "down"   : lambda d: (aim + d, depth, forward),
    }

    for line in f:
        action, d = line.strip().split()
        aim,depth,forward = dirs[action](int(d))

    print(f"Part 2: {depth * forward}")
