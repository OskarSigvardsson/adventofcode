from itertools import product

def debug(img):
    for line in img:
        print("".join('.' if c == 0 else '#' for c in line))
    print()

def enhance(img, table, bg):
    w,h = len(img[0]), len(img)

    def sample(x,y):
        if x in range(w) and y in range(h):
            return img[y][x]
        return bg

    img2 = [[0 for _ in range(w+2)] for _ in range(h+2)]
    
    for x,y in product(range(w+2), range(h+2)):
        n = 0
        for dy in [-2,-1,0]:
            for dx in [-2,-1,0]:
                n = 2*n + sample(x+dx, y+dy)

        img2[y][x] = table[n]

    return img2, table[511] if bg == 1 else table[0]

with open("input.txt") as f:
    table = [0 if c == '.' else 1 for c in f.readline().strip()]

    assert(len(table) == 512)

    f.readline()
    img = []
    bg = 0

    for line in f:
        img.append([0 if c == '.' else 1 for c in line.strip()])


    assert(all(len(line) == len(img[0]) for line in img))

    img2,bg2 = enhance(img, table, bg)
    img3,bg3 = enhance(img2, table, bg2)

    # debug(img2)
    # debug(img3)

    print(sum(sum(line) for line in img3))

    for _ in range(50):
        img,bg = enhance(img,table,bg)

    print(sum(sum(line) for line in img))
        
    
