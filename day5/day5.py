filename = "example1.txt"
# filename = "example2.txt"
filename = "input.txt"

lines = None
with open(filename, "r") as f:
    lines = f.readlines()

ans = 0

fresh: set[tuple[int, int]] = set()

# Part 1
# in_ingredients = False
# for line in lines:
#     if in_ingredients:
#         ingredient = int(line)
#         for x, y in fresh:
#             if ingredient >= x and ingredient <= y:
#                 ans += 1
#                 break
#     else:
#         if line == "\n":
#             in_ingredients = True
#             continue
#         a, b = map(int, line.split("-"))
#         fresh.add((a, b))

# Part 2
for line in lines:
    if line == "\n":
        break
    new_a, new_b = map(int, line.split("-"))
    added = False
    to_remove = set()
    for a, b in fresh:
        if new_a > b or new_b < a:
            continue
        elif new_a >= a and new_b <= b:
            added = True
        elif new_a >= a and new_b > b:
            new_a = b + 1
        elif new_a < a and new_b <= b:
            new_b = a - 1
        else:
            to_remove.add((a,b))

    if not added:
        fresh.add((new_a, new_b))
    for r in to_remove:
        fresh.remove(r)

for a, b in fresh:
    ans += b - a + 1


print(ans)
