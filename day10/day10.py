from itertools import combinations
from collections import Counter
from scipy.optimize import linprog
import numpy as np

filename = "example1.txt"
# filename = "example2.txt"
filename = "input.txt"

lines = None
with open(filename, "r") as f:
    lines = f.readlines()

ans = 0

# Part 1
for line in lines:
    parts = line.split()
    lights_str = parts[0]
    button_strs = parts[1:-1]

    lights = tuple(map(lambda c: 0 if c == "." else 1, lights_str[1:-1]))

    buttons = list()
    for button_str in button_strs:
        buttons.append(Counter(map(int, button_str[1:-1].split(","))))

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

# Part 2
ans = 0

for line in lines:
    parts = line.split()
    button_strs = parts[1:-1]
    joltage_str = parts[-1]

    buttons: list[tuple[int, ...]] = list()
    for button_str in button_strs:
        buttons.append(tuple(map(int, button_str[1:-1].split(","))))

    joltage = tuple(map(int, joltage_str[1:-1].split(",")))

    c = np.ones(len(buttons), dtype=int)
    integrality = np.ones_like(c)
    A_eq = []
    for i in range(len(joltage)):
        A_eq.append([])
        for button in buttons:
            if i in button:
                A_eq[i].append(1)
            else:
                A_eq[i].append(0)
    A_eq = np.array(A_eq)
    b_eq = np.array(joltage)
    res = linprog(c, A_eq=A_eq, b_eq=b_eq, integrality=integrality)
    ans += int(sum(res.x))


print(ans)
