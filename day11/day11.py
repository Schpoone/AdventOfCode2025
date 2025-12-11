from functools import lru_cache

filename = "example1.txt"
filename = "example2.txt"
filename = "input.txt"

lines = None
with open(filename, "r") as f:
    lines = f.readlines()

ans = 0

devices = dict()

for line in lines:
    parts = line.split(": ")
    devices[parts[0]] = parts[1].split()

# Part 1
# def paths_to_out(start: str) -> int:
#     if "out" in devices[start]:
#         return 1
#     num = 0
#     for output in devices[start]:
#         num += paths_to_out(output)
#     return num
# print(paths_to_out("you"))

# Part 2
@lru_cache(10000)
def paths_to_out_containing_reqs(start: str, dac: bool, fft: bool) -> int:
    if start == "dac":
        dac = True
    elif start == "fft":
        fft = True
    if "out" in devices[start]:
        if dac and fft:
            return 1
        else:
            return 0
    num = 0
    for output in devices[start]:
        num += paths_to_out_containing_reqs(output, dac, fft)
    return num
print(paths_to_out_containing_reqs("svr", False, False))
