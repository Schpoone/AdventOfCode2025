from collections import Counter

filename = "example1.txt"
# filename = "example2.txt"
filename = "input.txt"

lines = None
with open(filename, "r") as f:
    lines = f.readlines()

# Part 1
# ans = 0
# beams = set()
#
# for _, line in enumerate(lines):
#     for x, c in enumerate(line):
#         if c == "S":
#             beams.add(x)
#         elif c == "^":
#             if x in beams:
#                 ans += 1
#                 beams.remove(x)
#                 beams.add(x-1)
#                 beams.add(x+1)
#
# print(ans)

# Part 2
beams = Counter()

for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c == "S":
            beams[x] += 1
        elif c == "^":
            if x in beams:
                beams[x-1] += beams[x]
                beams[x+1] += beams[x]
                beams[x] = 0
print(sum(beams.values()))
