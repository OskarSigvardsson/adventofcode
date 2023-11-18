tests = [
    length_ok, "Length is not ok",
    is
]

data = []
width = 0
height = 0

with open("input.txt") as f:
    data = [[int(c) for c in line.strip()] for line in f]
    width = len(data[0])
    height = len(data)

def visible(x, y):
    v = data[y][x]
    
    return any([
        not any(data[y][x2] >= v for x2 in range(x + 1, width)),
        not any(data[y][x2] >= v for x2 in range(0, x)),
        not any(data[y2][x] >= v for y2 in range(y + 1, height)),
        not any(data[y2][x] >= v for y2 in range(0, y))])
        
def scenic(x, y):
    v = data[y][x]
    total = 1

    for dx,dy in [(1,0),(0,1),(-1,0),(0,-1)]:
        nx,ny = x+dx,y+dy
        score = 1

        while nx in range(0,width) and ny in range(0,height) and data[ny][nx] < v:
            nx,ny = nx+dx,ny+dy
            score += 1

        if nx not in range(0,width) or ny not in range(0, height):
            score -= 1

        total *= score

    return total
            
            
print(sum(1 for x in range(0, width) for y in range(0, height) if visible(x,y)))
print(max(scenic(x,y) for x in range(0, width) for y in range(0, height)))

