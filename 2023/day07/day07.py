import re

with open("../inputs/day07-test.txt", "r") as f:
    lines = f.readlines()
    time = [int(n) for n in re.findall("\d+", lines[0])]
    dist = [int(n) for n in re.findall("\d+", lines[1])]
    race = list(zip(time,dist))

    print(race)

