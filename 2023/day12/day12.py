# this is a test generator for debugging. given a line and the groups of
# numbers, it generates all possible solutions. it's messy, lots of corner cases
# that could have been handled better, but it works.
#
# slow also. just used this as a basis for gen2, the memoized version that does
# the counting correctly. 
#
# the g parameter is weird, it basically just indicates "are we currently in a
# group that needs to continue?"
def gen(line, ns, g = False, indent = 0):
    print(" " * indent + "".join(line),ns)

    if line == () and (ns == () or ns == (0,)):
        # we're at the end, and have no numbers left, so yield one valid solution
        yield ()
        return
    elif line == ():
        # we're at the end, but numbers are still left, so yield no valid solutions
        return
    elif line[0] == "?":
        # we're at a question mark, try both ways
        yield from gen((".",) + line[1:], ns, g, indent)
        yield from gen(("#",) + line[1:], ns, g, indent)

    elif len(ns) > 0 and ns[0] == 0:
        # the first group is "length 0", which is only valid if the next is a
        # ".". If so, recurse
        if line[0] == ".":
            yield from gen(line, ns[1:], False, indent)
            
    elif line[0] == ".":
        # if we're at a dot, but in a group that has to continue, this is not a valid sln
        if g: return
        
        # if we're not in a group, sln is valid so far, recurse
        for sl in gen(line[1:], ns, False, indent + 1):
            yield (".",) + sl
            
    elif line[0] == "#":
        if ns == ():
            # if there are no groups left, this is not a valid sln
            return
        elif ns[0] == 0:
            # if ns[0] == 0, the group should have ended, this s not a valid sln
            return
        else:
            # reduce first group number by one, recurse
            ns2 = (ns[0] - 1,) + ns[1:]
            for sl in gen(line[1:], ns2, True, indent + 1):
                yield ("#",) + sl

# memoized version of gen()
memo = {}
def gen2(line, ns, g = False, indent = 0):
    #print(" " * indent + "".join(line),ns)

    if line == () and (ns == () or ns == (0,)):
        return 1
    elif line == ():
        return 0
    elif (line,ns,g) in memo:
        return memo[(line, ns, g)]
    elif line[0] == "?":
        s  = gen2((".",) + line[1:], ns, g, indent)
        s += gen2(("#",) + line[1:], ns, g, indent)

        memo[(line, ns, g)] = s
        return s
    
    elif len(ns) > 0 and ns[0] == 0:
        if line[0] == ".":
            s = gen2(line, ns[1:], False, indent)
            memo[(line,ns,g)] = s
            return s
        else:
            return 0
            
    elif line[0] == ".":
        if g: return 0
        
        s = gen2(line[1:], ns, False, indent + 1)
        memo[(line,ns,g)] = s
        return s

            
    elif line[0] == "#":
        if ns == ():
            return 0
        elif ns[0] == 0:
            return 0
        else:
            ns2 = (ns[0] - 1,) + ns[1:]
            s = gen2(line[1:], ns2, True, indent + 1)
            memo[(line,ns,g)] = s
            return s


def intersperse(seq, copies, delim):
    for i in range(copies):
        yield from seq
        if i != copies - 1:
            yield delim

with open("../inputs/day12-real.txt", "r") as f:
    inputs = []

    for line in f:
        m,ns = line.strip().split(" ")
        inputs.append((tuple(m),tuple(int(n) for n in ns.split(","))))

    part1 = sum(gen2(m, ns) for m,ns in inputs)

    print(f"Part 1 {part1}")

    for i,vs in enumerate(inputs):
        m,ns = vs

        inputs[i] = (tuple(intersperse(m, 5, "?")), ns * 5)

    print("".join(inputs[0][0]), inputs[0][1])
    part2 = sum(gen2(m, ns) for m,ns in inputs)

    print(f"Part 2 {part2}")
