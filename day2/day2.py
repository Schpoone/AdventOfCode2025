

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
        id_good = False
        for j in range(1, len(id)//2+1):
            if len(id) % j != 0:
                continue
            good = True
            for k in range(j, len(id), j):
                if id[:j] != id[k:k+j]:
                    good = False
                    break
            if good:
                id_good = True
                break
        if id_good:
            ans += i

print(ans)
