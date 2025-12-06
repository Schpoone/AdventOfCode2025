

filename = "example1.txt"
# filename = "example2.txt"
filename = "input.txt"

lines = None
with open(filename, "r") as f:
    lines = f.readlines()

# Part 1
# opts = lines[-1].split()
# cols = list()
# for op in opts:
#     if op == "+":
#         cols.append(0)
#     else:
#         cols.append(1)
#
# for line in lines[:-1]:
#     for idx, num in enumerate(line.split()):
#         if opts[idx] == "+":
#             cols[idx] += int(num)
#         else:
#             cols[idx] *= int(num)
# print(sum(cols))


# Part 2
ans = 0

opts: list[str] = list()
widths: list[int] = list()
for c in lines[-1].strip("\n"):
    if c == " ":
        widths[-1] += 1
    elif c == "+":
        opts.append("+")
        widths.append(0)
    else:
        opts.append("*")
        widths.append(0)
widths[-1] += 1

"""
Convert the characters in the columns
e.g.

123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  

      |
      v

[['1', '24', '356'], ['369', '248', '8'], ['32', '581', '175'], ['623', '431', '4']]

"""
digits: list[list[str]] = list(list("" for _ in range(widths[idx])) for idx in range(len(widths))) # list of the column sections which are lists of the digit columns
for line in lines[:-1]:
    col_idx = 0
    c_idx = 0
    for c in line.strip("\n"):
        if c_idx >= widths[col_idx]:
            col_idx += 1
            c_idx = 0
            continue
        if c == " ":
            c_idx += 1
            continue
        digits[col_idx][c_idx] += c
        c_idx += 1

for idx, col in enumerate(digits):
    if opts[idx] == "+":
        ans += sum(map(int, col))
    else:
        prod = 1
        for num in col:
            prod *= int(num)
        ans += prod

print(ans)
