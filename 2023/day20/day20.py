import re

from collections import deque
from math import lcm

class Module:
    def __init__(self, name):
        self.name = name
        self.ins = []
        self.outs = []

    def connect_in(self, other):
        self.ins.append(other)

    def connect_out(self, other):
        self.outs.append(other)
        
    def send(self, signal):
        return [(signal,self.name,module) for module in self.outs]

    def prepare(self): pass
    def pulse(self, sender, signal): pass

class Simple(Module):
    def pulse(self, sender, signal):
        return self.send(signal)

class FlipFlop(Module):
    def prepare(self):
        self.state = 0
        
    def pulse(self, sender, signal):
        if signal == 0:
            self.state = 1 - self.state
            return self.send(self.state)

        return []

class Conjunction(Module):
    def prepare(self):
        self.state = {sender:0 for sender in self.ins}
        
    def pulse(self, sender, signal):
        self.state[sender] = signal

        if all(s == 1 for s in self.state.values()):
            return self.send(0)
        else:
            return self.send(1)


outs = {}
modules = {}

with open("../inputs/day20-real.txt", "r") as f:
    for line in f:
        t,name,outstr = re.match("(&|%)?(\w+) -> (.*)", line).groups()
        name = name.strip()
        outs[name] = [s.strip() for s in outstr.strip().split(",")]

        match t:
            case "&":  modules[name] = Conjunction(name)
            case "%":  modules[name] = FlipFlop(name)
            case None: modules[name] = Simple(name)


    for source,v in outs.items():
        for dest in v:
            if dest not in modules:
                modules[dest] = Simple(dest)
                
            modules[source].connect_out(dest)
            modules[dest].connect_in(source)
    

def part1():
    for mod in modules.values():
        mod.prepare()

    q = deque()

    highs = 0
    lows = 0
    
    for _ in range(1000):
        q.append((0,"button","broadcaster"))

        while len(q) > 0:
            signal,sender,receiver = q.popleft()

            match signal:
                case 0: lows += 1
                case 1: highs += 1
                
            #hilo = "high" if signal == 1 else "low"
            #print(f"{sender} -{hilo}-> {receiver}")

            pulses = modules[receiver].pulse(sender, signal)
            q.extend(pulses)

        #print("---------------------")

    return highs * lows

def part2():
    for mod in modules.values():
        mod.prepare()

    q = deque()

    highs = 0
    lows = 0

    # the only input to "rx" is "bq", and "bq" has four different inputs. each
    # input comes from a self-contained part of the graph that eventually spits
    # out a 1 on some cycle. bq (and therefore rx) turns on when all these four
    # sync up, so the answer is the LCM of the cycles of these four nodes
    cycles = {name:0 for name in modules["bq"].ins}
    
    iters = 0
    while True:
        q.append((0,"button","broadcaster"))
        iters += 1

        while len(q) > 0:
            signal,sender,receiver = q.popleft()

            match signal:
                case 0: lows += 1
                case 1: highs += 1
                

            if signal == 1 and sender in cycles:
                cycles[sender] = iters

                if all(v > 0 for v in cycles.values()):
                    return lcm(*cycles.values())

            pulses = modules[receiver].pulse(sender, signal)
            q.extend(pulses)

        #print("---------------------")

    return highs * lows

print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
