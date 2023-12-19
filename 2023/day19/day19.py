import re

states = {}
orelse = {}
inputs = []

with open("../inputs/day19-real.txt", "r") as f:
    for line in f:
        if m := re.match(R"(\w+)\{(.*),(\w+)\}", line):
            state,instructions,final = m.groups()
            states[state] = []
            orelse[state] = final
            
            for inst in instructions.split(","):
                v,op,c,then = re.match(R"([xmas])([<>])(\d+):(\w+)",inst).groups()
                states[state].append((v,op,int(c),then))
            
        elif m := re.match(R"\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}", line):
            x,m,a,s = [int(n) for n in m.groups()]
            inputs.append({"x":x,"m":m,"a":a,"s":s})
    

# part 1
def comp(n, op, c):
    if op == "<": return n < c
    if op == ">": return n > c
    
def evaluate(vals, state = "in"):
    if state in ["A","R"]:
        return state
    
    for v,op,c,then in states[state]:
        if comp(vals[v],op,c):
            return evaluate(vals,then)

    return evaluate(vals, orelse[state])

part1 = sum(sum(ins.values()) for ins in inputs if evaluate(ins) == "A")
print(f"Part 1: {part1}")

# part 2
# idea is to pass whole ranges of numbers through the rules. the initial range is like
#
#    rng = {
#        "x":(1,4000),
#        "m":(1,4000),
#        "a":(1,4000),
#        "s":(1,4000)
#    }
#
# and if you pass that through the rule "x<2000", you get two new ranges: the
# first range is the range where this is true, the second is the range where
# this is false. so like:
#
#    truerng = {
#        "x":(1,1999),
#        "m":(1,4000),
#        "a":(1,4000),
#        "s":(1,4000)
#    }
#    falserng = {
#        "x":(2000,4000),
#        "m":(1,4000),
#        "a":(1,4000),
#        "s":(1,4000)
#    }
#
# then you evaluate those recursively. when you get to A, you count the valid
# results.
#
# nomenclature: a "span" is a single span of numbers like (2000,4000). a "range"
# is made up of four spans, one for each variable

# split a single span based on an operator and a constant
def splitspan(op, c, span):
    minv,maxv = span
    if op == "<":
        if c <= minv:
            return (None, span)
        if maxv < c:
            return (span, None)

        return ((minv, c-1),(c,maxv))
    if op == ">":
         if c >= maxv:
             return (None, span)
         if minv > c:
             return (span, None)

         return ((c+1,maxv),(minv,c))
    
# split a whole range
def splitrange(rng,v,op,c):
    sp1,sp2 = splitspan(op,c,rng[v])

    if sp1 == None:
        return (None,rng)
    if sp2 == None:
        return (rng,None)

    rng1 = dict(rng)
    rng2 = dict(rng)

    rng1[v] = sp1
    rng2[v] = sp2

    return (rng1,rng2)
    
# count valid of passing a range to a given state
def count(rng, state = "in"):
    if state == "R":
        return 0

    if state == "A":
        s = 1

        for a,b in rng.values():
            s *= b-a+1

        return s

    curr = rng
    s = 0
    
    for v,op,c,then in states[state]:
        sp1,sp2 = splitrange(curr, v, op, c)

        if sp1:
            s += count(sp1, then)

        curr = sp2

        if curr is None: break
    else:
        s += count(curr, orelse[state])

    return s

   
part2 = count({"x":(1,4000), "m":(1,4000), "a":(1,4000), "s":(1,4000)})
print(f"Part 2: {part2}")
