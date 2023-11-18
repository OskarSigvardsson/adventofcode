import re

filename = "input.txt"
form = re.compile(R"#(.*) @ (.*),(.*): (.*)x(.*)")
size = 1000
field = [0] * size**2

def debug(field):
    i = 0
    for y in range(size):
        for x in range(size):
            print(field[i], end='')
            i+=1
        print()

    
with open(filename) as f:
    for line in f:
        idn,sx,sy,w,h = (int(s) for s in form.match(line).groups())

        for x in range(sx, sx+w):
            for y in range(sy, sy+h):
                field[x + y * size] += 1

    #debug(field)
    print(sum(1 for n in field if n >= 2))

with open(filename) as f:
    for line in f:
        idn,sx,sy,w,h = (int(s) for s in form.match(line).groups())
        alone = True
        
        for x in range(sx, sx+w):
            for y in range(sy, sy+h):
                if field[x + y * size] != 1:
                    alone = False
                    break

            if not alone:
                break
            
        if alone:
            print(idn)
                    


                       
