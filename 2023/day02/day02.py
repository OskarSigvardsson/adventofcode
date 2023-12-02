import re

with open("../inputs/day02-real.txt") as f:

    games = {}

    for line in f:
        gid = int(re.match("Game (\d+): ", line).group(1))
        l = []

        for draw in (line.split(":")[1].split(";")):
            d = { 'red': 0, 'green': 0, 'blue': 0 }
            d.update({ mc[1]: int(mc[0]) for mc in re.findall("(\d+) (\w+)", draw) })

            l.append(d)

        games[gid] = l

    def check_draw(draw):
        return draw['red'] <= 12 and draw['green'] <= 13 and draw['blue'] <= 14

    possible = [gid for gid,game in games.items() if all(check_draw(draw) for draw in game)]

    print("Part 1: {}".format(sum(possible)))

    def min_for_game(game):
        mr = max(draw['red']   for draw in game)
        mg = max(draw['green'] for draw in game)
        mb = max(draw['blue']  for draw in game)

        return (mr,mg,mb)

    powers = [mr*mg*mb for (mr,mg,mb) in (min_for_game(game) for game in games.values())]

    print("Part 2: {}".format(sum(powers)))



