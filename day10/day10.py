from itertools import combinations
from collections import Counter

filename = "example1.txt"
# filename = "example2.txt"
filename = "input.txt"

lines = None
with open(filename, "r") as f:
    lines = f.readlines()

ans = 0

for line in lines:
    parts = line.split()
    lights_str = parts[0]
    button_strs = parts[1:-1]
    joltage = parts[-1]

    lights = tuple(map(lambda c: 0 if c == "." else 1, lights_str[1:-1]))
    print(lights)

    buttons = list()
    for button in button_strs:
        buttons.append(Counter(map(int, button[1:-1].split(","))))
    print(buttons)

    best = 0
    for i in range(len(buttons)):
        for combo in combinations(buttons, i):
            final_state = Counter()
            for button in combo:
                final_state = final_state + button
            for idx, light_state in enumerate(lights):
                if light_state != final_state[idx] % 2:
                    break
            else:
                best = i
                ans += best
            if best > 0:
                break
        if best > 0:
            break

print(ans)
