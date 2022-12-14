from collections import deque, defaultdict
from heapq import heappush, heappop

alphabet = "abcdefghijklmnopqrstuvwxyz"

w,h = 0,0
s,e = 0,0
m = defaultdict(lambda: 10000)

with open("input.txt") as f:
    for y,line in enumerate(f):
        h = y + 1
        w = len(line.strip())
        
        for x,c in enumerate(line.strip()):
            if c == "S":
                s = (x,y)
            elif c == "E":
                e = (x,y)
            else:
                m[(x,y)] = alphabet.index(c)

    m[s] = alphabet.index("a")
    m[e] = alphabet.index("z")

def part1():
    visited = set()
    queue = deque([(0,s)])
    
    while len(queue) > 0:
        steps,p = queue.popleft()

        px,py = p
        
        if p == e:
            return steps
        
        if p in visited:
            continue

        v = m[p]

        visited.add(p)

        if m[(px+1,py)] <= v + 1: queue.append((steps+1,(px+1,py)))
        if m[(px-1,py)] <= v + 1: queue.append((steps+1,(px-1,py)))
        if m[(px,py+1)] <= v + 1: queue.append((steps+1,(px,py+1)))
        if m[(px,py-1)] <= v + 1: queue.append((steps+1,(px,py-1)))

    return result

def part2():
    visited = set()
    queue = deque([(0,e)])
    
    while len(queue) > 0:
        steps,p = queue.popleft()
        px,py = p
        v = m[p]
        
        if v == 0:
            return steps
        
        if p in visited:
            continue

        visited.add(p)

        if m[(px+1,py)] >= v - 1: queue.append((steps+1,(px+1,py)))
        if m[(px-1,py)] >= v - 1: queue.append((steps+1,(px-1,py)))
        if m[(px,py+1)] >= v - 1: queue.append((steps+1,(px,py+1)))
        if m[(px,py-1)] >= v - 1: queue.append((steps+1,(px,py-1)))

    return result

print(part1())
print(part2())
