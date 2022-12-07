import re

with open("input.txt") as f:
    files = {}
    folders = {"/": 0}
    curr = [""]
    
    for line in f:
        if m := re.match(R"[$] cd (.+)$", line):
            d = m.group(1)

            if d == "..":
                curr = curr[:-1]
            elif d == "/":
                curr = [""]
            else:
                curr.append(d)
                folders["/".join(curr) + "/"] = 0

        elif m := re.match(R"(\d+) (.+)", line):
            files[f"{'/'.join(curr)}/{m.group(2)}"] = int(m.group(1))

        else:
            pass

    for folder in folders.keys():
        for f,s in files.items():
            if f.startswith(folder):
                folders[folder] += s

    small_folders = 0
    for folder,size in folders.items():
        if size <= 100000:
            small_folders += size

    print(small_folders)

    max_space = 70000000
    req_space = 30000000
    curr_space = folders["/"]
    min_delete = float('inf')

    for folder,size in folders.items():
        if max_space - (curr_space - size) > req_space:
            min_delete = min(min_delete, size)

    print(min_delete)
