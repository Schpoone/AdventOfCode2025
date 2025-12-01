

filename = "example1.txt"
# filename = "example2.txt"
filename = "input.txt"

lines = None
with open(filename, "r") as f:
    lines = f.readlines()

ans = 0
pointer = 50
for line in lines:
    old_pointer = pointer
    rot = int(line[1:])
    ans += rot // 100
    rot = rot % 100
    if line[0] == "L":
        if pointer - rot <= 0 and pointer != 0:
            ans += 1
        pointer -= rot
    else:
        if pointer + rot >= 100:
            ans += 1
        pointer += rot
    pointer = (pointer + 100) % 100

print(ans)
