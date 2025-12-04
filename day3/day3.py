
filename = "example1.txt"
# filename = "example2.txt"
filename = "input.txt"

lines = None
with open(filename, "r") as f:
    lines = f.readlines()

def greatest_joltage(substring: str, num_batt: int) -> int:
    if num_batt > len(substring):
        return 0
    if num_batt == 1:
        best = max(int(c) for c in substring)
        return best
    best = max(int(c) for c in substring[:-num_batt+1])
    best_idx = substring.find(str(best))
    second_part = greatest_joltage(substring[best_idx+1:], num_batt - 1)
    return int(str(best) + str(second_part))

ans = 0

for line in lines:
    line = line.strip()
    joltage = greatest_joltage(line, 12)
    ans += joltage

print(ans)
