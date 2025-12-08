

filename = "example1.txt"
# filename = "example2.txt"
filename = "input.txt"

lines = None
with open(filename, "r") as f:
    lines = f.readlines()

ans = 0

vec = tuple[int, ...]

boxes: list[vec] = list()
for line in lines:
    boxes.append(tuple(map(int, line.split(","))))

# Calculate distances between each box pair
distances = list()
distance_map: dict[int, tuple[vec, vec]] = dict()
for box1 in boxes:
    for box2 in boxes:
        distance = (box2[0]-box1[0])**2 + (box2[1]-box1[1])**2 + (box2[2]-box1[2])**2
        if box1 == box2 or (box2, box1) == distance_map.get(distance):
            continue
        distance_map[distance] = (box1, box2)
        distances.append(distance)

distances.sort()

# Join boxes together into circuits
circuits: list[set[vec]] = list()
for distance in distances:
    box1, box2 = distance_map[distance]
    need_merge = list()
    for circuit in circuits:
        if box1 in circuit or box2 in circuit:
            need_merge.append(circuit)
    if not need_merge:
        circuits.append(set([box1, box2]))
    elif len(need_merge) == 1:
        need_merge[0].add(box1)
        need_merge[0].add(box2)
    elif len(need_merge) > 1:
        new_circuit: set[vec] = set()
        for circuit in need_merge:
            new_circuit = new_circuit.union(circuit)
            circuits.remove(circuit)
        circuits.append(new_circuit)
    if len(circuits) == 1 and len(circuits[0]) == len(boxes):
        print(box1[0] * box2[0])
        break
