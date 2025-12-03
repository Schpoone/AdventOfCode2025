from functools import lru_cache

filename = "example1.txt"
# filename = "example2.txt"
filename = "input.txt"

lines = None
with open(filename, "r") as f:
    lines = f.readlines()

@lru_cache(1000)
def greatest_joltage(substring: str, num_batt: int) -> int:
    if num_batt > len(substring):
        return 0
    if num_batt == 1:
        best = max(int(c) for c in substring)
        return best
    subjolt1 = greatest_joltage(substring[1:], num_batt)
    subjolt2 = greatest_joltage(substring[1:], num_batt - 1)
    best = max(subjolt1, int(substring[0] + str(subjolt2)))
    return best

ans = 0

for line in lines:
    line = line.strip()
    joltage = greatest_joltage(line, 12)
    ans += joltage

print(ans)
