import re

ranges = []
ids = []

for line in open("../inputs/day05-real.txt"):
	if line.strip() == "": 
		continue

	match line.split("-"):
		case [beg, end]: ranges.append((int(beg), int(end)))
		case [id]: ids.append(int(id))
	
# Part 1
def is_fresh(id):
	return any(beg <= id <= end for (beg,end) in ranges)

part1 = sum(is_fresh(id) for id in ids)

# Part 2

# this is a weird name for a variable, but i think of this as a list of
# "events", where each event is "range has started" or "range has ended". if we
# scan through the events in order, as long as there's at least one range
# started, we're fresh
events = []
for (beg, end) in ranges:
	events.append((beg, "beg"))
	events.append((end, "end"))
events.sort()

i = 0
part2 = 0
count = 0

for (id, event) in events:
	if count > 0:
		part2 += id - i
	
	if event == "beg":
		count += 1
	if event == "end":
		count -= 1
		
		# this is annoying, but otherwise we get off-by-one errors because the
		# range is inclusive on both ends
		if count == 0:
			part2 += 1

	i = id

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")