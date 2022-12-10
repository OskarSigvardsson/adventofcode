import re

lines = []

with open("input.txt") as f:
    lines = f.readlines()

x = 1
cycles = []

for line in lines:
    if line == "noop\n":
        cycles.append(x)
    elif m := re.match(R"addx (-?\d+)", line):
        cycles.append(x)
        cycles.append(x)
        x += int(m.group(1))

# part 1
print(sum(i*cycles[i-1] for i in range(20, 221, 40)))

# part 2
for y in range(6):
    for x in range(40):
        i = x + y * 40
        lit = abs(cycles[i] - x) <= 1
        print('#' if lit else ' ', end='')
    print()
