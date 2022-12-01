import re

from itertools import product

def day17(xmin,xmax,ymin,ymax):
    xr = range(xmin, xmax + 1)
    yr = range(ymin, ymax + 1)

    # xvs holds all the possible values of x velocities
    xvs = []

    for x in range(xmax + 1):
        xv = x
        xp = 0

        while xv > 0:
            xp += xv
            xv -= 1

            if xp in xr:
                xvs.append(x)
                break

    # yvs holds all the possible values of y velocities
    # (this could be done better :) )
    yvs = []

    for y in range(ymin - 1, -ymin + 1):
        yv = y
        yp = 0
    
        while yp >= ymin:
            yp += yv
            yv -= 1

            if yp in yr:
                yvs.append(y)
                break

    def sign(x):
        return x if x == 0 else int(x/abs(x))
    
    maxheight = 0
    vels = 0
    
    for x,y in product(xvs,yvs):
        xv,yv = x,y
        xp, yp = 0,0
        highest = 0
        
        while xp <= xmax and yp >= ymin:
            xp += xv
            yp += yv
            xv -= sign(xv)
            yv -= 1

            highest = max(highest, yp)

            if xp in xr and yp in yr:
                maxheight = max(maxheight, highest)
                vels += 1
                break

    return maxheight, vels


with open("input.txt", "r") as f:
    m = re.match(R"target area: x=(.*)\.\.(.*), y=(.*)\.\.(.*)$", f.readline())
    xmin, xmax, ymin, ymax = [int(g) for g in m.groups()]

    print(f"Day 17: { day17(xmin, xmax, ymin, ymax) }")
