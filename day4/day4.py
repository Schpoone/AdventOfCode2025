

filename = "example1.txt"
# filename = "example2.txt"
filename = "input.txt"

lines = None
with open(filename, "r") as f:
    lines = f.readlines()

ans = 0

grid = set()

for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c == '@':
            grid.add((x,y))

new_grid = set(grid)
keep_going = True
while keep_going:
    keep_going = False
    for x, y in grid:
        adj = [(x+1,y),(x+1,y+1),(x,y+1),(x-1,y),(x-1,y-1),(x-1,y+1),(x+1,y-1),(x,y-1)]
        if len([p for p in adj if p in grid]) < 4:
            ans += 1
            new_grid.remove((x,y))
            keep_going = True
    grid = set(new_grid)

print(ans)
