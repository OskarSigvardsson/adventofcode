
#part 1
with open("input.txt", "r") as f:
    lines = [list(reversed([int(c) for c in line.strip()])) for line in f]

    rows = len(lines)
    cols = len(lines[0])

    # PRO PYTHON HAXX!!!
    transposed = zip(*lines)

    gamma = sum(2**i if sum(v) > rows/2 else 0 for i,v in enumerate(transposed))

    # this does unsigned bitwise negation. can't use operator ~, because that
    # does signed negation.
    epsilon = (2**cols - 1) ^ gamma

    print(f"Part 1 { gamma * epsilon }")


#part 2
with open("input.txt", "r") as f:
    lines = [[int(c) for c in line.strip()] for line in f]

    cols = len(lines[0])

    oxy = lines[:]
    co2 = lines[:]

    # i probably wouldn't write these loops like this in production code, it's
    # too confusing. but fancy oneliners are what advent of code is for :)
    for i in range(cols):
        if len(oxy) == 1: break

        crit_oxy = 1 if (len([n for n in oxy if n[i] == 1]) >= len(oxy) / 2) else 0
        oxy = [line for line in oxy if line[i] == crit_oxy]


    for i in range(cols):
        if len(co2) == 1: break

        crit_co2 = 0 if (len([n for n in co2 if n[i] == 1]) >= len(co2) / 2) else 1
        co2 = [line for line in co2 if line[i] == crit_co2]

    oxy_n = sum(2**i * n for i,n in enumerate(reversed(oxy[0])))
    co2_n = sum(2**i * n for i,n in enumerate(reversed(co2[0])))

    print(f"Part 2: { co2_n * oxy_n }")


