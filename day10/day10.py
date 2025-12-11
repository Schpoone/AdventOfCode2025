from functools import cache
from itertools import combinations, combinations_with_replacement
from collections import Counter

filename = "example1.txt"
# filename = "example2.txt"
filename = "input.txt"

lines = None
with open(filename, "r") as f:
    lines = f.readlines()

ans = 0

# Part 1
# for line in lines:
#     parts = line.split()
#     lights_str = parts[0]
#     button_strs = parts[1:-1]
#
#     lights = tuple(map(lambda c: 0 if c == "." else 1, lights_str[1:-1]))
#     print(lights)
#
#     buttons = list()
#     for button in button_strs:
#         buttons.append(Counter(map(int, button[1:-1].split(","))))
#     print(buttons)
#
#     best = 0
#     for i in range(len(buttons)):
#         for combo in combinations(buttons, i):
#             final_state = Counter()
#             for button in combo:
#                 final_state = final_state + button
#             for idx, light_state in enumerate(lights):
#                 if light_state != final_state[idx] % 2:
#                     break
#             else:
#                 best = i
#                 ans += best
#             if best > 0:
#                 break
#         if best > 0:
#             break
#
# print(ans)

# Part 2
# TODO: Try going joltage counter by counter and only trying combos of buttons related to each counter
# TODO: Try integer programming
def counter_from_tuple(joltage_tuple: tuple[int, ...]) -> Counter[int]:
    joltage: Counter[int] = Counter()
    for idx, jolt in enumerate(joltage_tuple):
        joltage[idx] = jolt
    return joltage
def counter_to_tuple(joltage: Counter[int]) -> tuple[int, ...]:
    return tuple(joltage[i] for i in range(len(joltage)))
def joltage_from_buttons(buttons_tuple: tuple[tuple[int, ...], ...], buttons_pressed: tuple[int, ...]) -> Counter[int]:
    joltage: Counter[int] = Counter()
    for idx, num_presses in enumerate(buttons_pressed):
        for counter_idx in buttons_tuple[idx]:
            joltage[counter_idx] += num_presses
    return joltage


@cache
def least_buttons_for_joltage(buttons_tuple: tuple[tuple[int, ...]], joltage_tuple: tuple[int, ...]) -> int:
    joltage = counter_from_tuple(joltage_tuple)

    best = -2
    for button in buttons_tuple:
        new_joltage = Counter(joltage)
        new_joltage.subtract(button)
        if any(map(lambda j: j < 0, new_joltage.values())):
            continue
        if all(map(lambda j: j == 0, new_joltage.values())):
            return 1
        new_best = least_buttons_for_joltage(buttons_tuple, counter_to_tuple(new_joltage))
        if new_best < 0:
            continue
        if best < 0 or new_best < best:
            best = new_best
    return best + 1

least_buttons = -1
buttons_pressed_to_least_remaining_buttons_cache: dict[tuple[int, ...], int] = dict()
# Build up buttons_pressed without changing joltage_tuple
def least_remaining_buttons_for_joltage(buttons_tuple: tuple[tuple[int, ...], ...], joltage_tuple: tuple[int, ...], buttons_pressed: tuple[int, ...]) -> int:
    global least_buttons, buttons_pressed_to_least_remaining_buttons_cache
    joltage = counter_from_tuple(joltage_tuple)
    current_joltage = joltage_from_buttons(buttons_tuple, buttons_pressed)
    remaining_needed_joltage = Counter(joltage)
    remaining_needed_joltage.subtract(current_joltage)

    if buttons_pressed in buttons_pressed_to_least_remaining_buttons_cache:
        return buttons_pressed_to_least_remaining_buttons_cache[buttons_pressed]
    if least_buttons > 0 and sum(buttons_pressed) + max(remaining_needed_joltage.values()) > least_buttons:
        buttons_pressed_to_least_remaining_buttons_cache[buttons_pressed] = -1
        return -1
    if any(map(lambda j: j < 0, remaining_needed_joltage.values())):
        buttons_pressed_to_least_remaining_buttons_cache[buttons_pressed] = -1
        return -1
    if all(map(lambda j: j == 0, remaining_needed_joltage.values())):
        num_buttons = sum(buttons_pressed)
        if least_buttons < 0 or num_buttons < least_buttons:
            least_buttons = num_buttons
        return 0
    least_remaining_buttons = -1
    for idx in range(len(buttons_tuple)):
        new_buttons = counter_from_tuple(buttons_pressed)
        new_buttons[idx] += 1
        remaining_needed_buttons = least_remaining_buttons_for_joltage(buttons_tuple, joltage_tuple, counter_to_tuple(new_buttons))
        if remaining_needed_buttons < 0:
            continue
        if least_remaining_buttons < 0 or remaining_needed_buttons < least_remaining_buttons:
            least_remaining_buttons = remaining_needed_buttons + 1
    if least_remaining_buttons < 0:
        buttons_pressed_to_least_remaining_buttons_cache[buttons_pressed] = -1
        return -1
    buttons_pressed_to_least_remaining_buttons_cache[buttons_pressed] = least_remaining_buttons
    return least_remaining_buttons

for line in lines:
    print(line)
    parts = line.split()
    button_strs = parts[1:-1]
    joltage_str = parts[-1]

    buttons = list()
    for button in button_strs:
        buttons.append(tuple(map(int, button[1:-1].split(","))))

    joltage = tuple(map(int, joltage_str[1:-1].split(",")))

    # best = least_buttons_for_joltage(tuple(buttons), joltage)
    # ans += best
    best = least_remaining_buttons_for_joltage(tuple(buttons), joltage, tuple([0]*len(buttons)))
    ans += best
    least_buttons = -1
    buttons_pressed_to_least_remaining_buttons_cache.clear()

print(ans)
