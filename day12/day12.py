

filename = "example1.txt"
# filename = "example2.txt"
filename = "input.txt"

input = None
with open(filename, "r") as f:
    input = f.read()

# Parsing
presents: list[set[tuple[int, int]]] = list()
regions: list[str] = list()
requirements: list[list[int]] = list()

parts = input.split("\n\n")
for part in parts:
    if "#" in part:
        grid = part.split("\n")[1:]
        present = set()
        for y, line in enumerate(grid):
            for x, c in enumerate(line):
                if c == "#":
                    present.add((x,y))
        presents.append(present)
    else:
        for line in part.strip().split("\n"):
            region, req_presents = line.split(": ")
            regions.append(region)
            requirements.append(list(map(int, req_presents.split())))

lower_bound = 0
upper_bound = 0

for region, req in zip(regions, requirements):
    region_size = tuple(map(int, region.split("x")))
    total_present_area = sum(n*len(presents[i]) for i, n in enumerate(req))
    max_present_area = sum(n*9 for n in req)
    if region_size[0]*region_size[1] < total_present_area:
        continue
    upper_bound += 1
    if region_size[0]*region_size[1] < max_present_area:
        continue
    lower_bound += 1

print("Lower bound:", lower_bound)
print("Upper bound:", upper_bound)
