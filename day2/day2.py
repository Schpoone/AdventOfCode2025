

filename = "example1.txt"
# filename = "example2.txt"
filename = "input.txt"

lines = None
with open(filename, "r") as f:
    lines = f.read().split(",")

ans = 0

for line in lines:
    id1, id2 = map(int, line.split("-"))
    for i in range(id1, id2+1):
        id = str(i)
        for j in range(1, len(id)//2+1):
            if id[0] != id[j]:
                continue
            if len(id) % j != 0:
                continue
            if id == (id[:j] * (len(id)//j)):
                ans += i
                break

print(ans)
