from itertools import product

import re

def part1(instructions):
    cubes = set()

    for onoff,coords in instructions:
        x0,x1,y0,y1,z0,z1 = coords
        it = product(range(x0,x1+1), range(y0,y1+1), range(z0,z1+1))
        
        if onoff == "on":
            cubes.update(it)
        else:
            cubes.difference_update(it)

    return len(cubes)

def intersect_ranges(a0,a1,b0,b1):
    if a0 <= b0 <= a1:
        return (b0, min(b1,a1))
    if a0 <= b1 <= a1:
        return (max(a0,b0), b1)

def intersect_cuboids(c1, c2):
    x00,x01,y00,y01,z00,z01 = c1
    x10,x11,y10,y11,z10,z11 = c2

    xi = intersect_ranges(x00, x01, x10, x11)
    yi = intersect_ranges(y00, y01, y10, y11)
    zi = intersect_ranges(z00, z01, z10, z11)
    
    if xi and yi and zi:
        x20,x21 = xi
        y20,y21 = yi
        z20,z21 = zi

        return (x20,x21,y20,y21,z20,z21)

class Cuboids:
    add = []
    subtract = []
    levels = []

    def add_level(self, cuboid, level):
        if len(self.levels) == level:
            self.levels.append([cuboid])
        else:

            inters = set([intersect_cuboids(c, cuboid) for c in self.levels[level]])
            self.levels[level].append(cuboid)

            for inter in inters:
                if inter:
                    self.add_level(inter, level + 1)

    def sub(self, cuboid):
        inters = [intersect_cuboids(c, cuboid) for c in self.levels[0]]

        for inter in inters:
            if inter:
                self.add_level(inter, 1)
        

    def count_level(self):
        total = 0
        mul = 1

        for level in self.levels:
            for cuboid in level:
                x0,x1,y0,y1,z0,z1 = cuboid

                dx = x1 - x0 + 1
                dy = y1 - y0 + 1
                dz = z1 - z0 + 1

                total += mul * dx * dy * dz

            mul *= -1

        return total


    def __iadd__(self, cuboid):
        if cuboid in self.add:
            return self
        
        if cuboid in self.subtract:
            self.subtract.remove(cuboid)
            return self
        
        intersections = [intersect_cuboids(c, cuboid) for c in self.add]
        self.add.append(cuboid)
        
        for inter in intersections:
            if inter:
                print(f"Inter: { inter }")
                self -= inter

        return self

        
    def __isub__(self, cuboid):
        if cuboid in self.subtract:
            return self

        
        if cuboid in self.add:
            self.add.remove(cuboid)
            return self
        
        intersections = [intersect_cuboids(c, cuboid) for c in self.subtract]
        self.subtract.append(cuboid)
        
        for inter in intersections:
            if inter:
                print(f"Inter: { inter }")
                self += inter

        return self

    def count(self):
        print(f"Add: { self.add }")
        print(f"Sub: { self.subtract }")
        total = 0

        for x0,x1,y0,y1,z0,z1 in self.add:
            dx = x1 - x0 + 1
            dy = y1 - y0 + 1
            dz = z1 - z0 + 1

            total += dx * dy * dz

        for x0,x1,y0,y1,z0,z1 in self.subtract:
            dx = x1 - x0 + 1
            dy = y1 - y0 + 1
            dz = z1 - z0 + 1

            total -= dx * dy * dz

        return total
    
def part2(instructions):
    cubes = Cuboids()

    for onoff,coords in instructions:
        print(f"Instruction: { onoff }, { coords }")
        if onoff == "on":
            #cubes += coords
            cubes.add_level(coords, 0)
        else:
            pass
            #cubes -= coords
            #cubes.sub(coords)
            cubes.sub(coords)

        # print(f"Levels: { cubes.levels }")
        # print(f"Count: { cubes.count_level() }")

    return cubes.count_level()
    
    
with open("test.txt", "r") as f:
    regex = re.compile(R"(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=-(-?\d+)\.\.(-?\d+)")
    regex = re.compile(R"(on|off) x=(.*)\.\.(.*),y=(.*)\.\.(.*),z=(.*)\.\.(.*)")

    part1ins = []
    part2ins = []

    for line in f:
        gs = regex.match(line).groups()
        coords = tuple(int(g) for g in gs[1:])
        x0,x1,y0,y1,z0,z1 = coords

        assert(x0 <= x1)
        assert(y0 <= y1)
        assert(z0 <= z1)

        if all(c in range(-50, 51) for c in coords):
            part1ins.append((gs[0], coords))

        part2ins.append((gs[0], coords))
        
    with open("test2cpp.txt", "w") as f2:
        for ins in part2ins:
            onoff = ins[0]
            x0,x1,y0,y1,z0,z1 = ins[1]

            if onoff == "on":
                f2.write(f"coll += Quad({x0},{y0},{z0},{x1},{y1},{z1});\n")
            else:
                f2.write(f"coll -= Quad({x0},{y0},{z0},{x1},{y1},{z1});\n")
            
    # c1 = (10, 12, 10, 12, 10, 12)
    # c2 = (11, 13, 11, 13, 11, 13)
    # print(f"Intersection range: { intersect_ranges(10,12,11,13) }")
    # print(f"Intersection: { intersect_cuboids(c1, c2) }")

    
    # print(f"Part 1: { part1(part1ins) } ")
    # print(f"Part 2: { part2(part1ins) } ")
