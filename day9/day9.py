from tqdm import tqdm

filename = "example1.txt"
# filename = "example2.txt"
filename = "input.txt"

lines = None
with open(filename, "r") as f:
    lines = f.readlines()


### Part 1 was trivial so it is NOT included here ###


def get_edge_direction(p, q):
    if p[0] == q[0]:
        if p[1] > q[1]:
            return "U"
        else:
            return "D"
    else:
        if p[0] > q[0]:
            return "L"
        else:
            return "R"

def edge_intersects_rect(edge1, edge2, corner1, corner2):
    min_x = min(corner1[0], corner2[0])
    max_x = max(corner1[0], corner2[0])
    min_y = min(corner1[1], corner2[1])
    max_y = max(corner1[1], corner2[1])
    dir = get_edge_direction(edge1, edge2)
    if dir in "LR":
        edge_y = edge1[1]
        edge_min_x = min(edge1[0], edge2[0])
        edge_max_x = max(edge1[0], edge2[0])
        return min_y < edge_y < max_y and edge_max_x > min_x and edge_min_x < max_x
    elif dir in "UD":
        edge_x = edge1[0]
        edge_min_y = min(edge1[1], edge2[1])
        edge_max_y = max(edge1[1], edge2[1])
        return min_x < edge_x < max_x and edge_max_y > min_y and edge_min_y < max_y

def point_in_edge(p, edge1, edge2):
    dir = get_edge_direction(edge1, edge2)
    if dir in "LR":
        min_x = min(edge1[0], edge2[0])
        max_x = max(edge1[0], edge2[0])
        return p[1] == edge1[1] and min_x <= p[0] <= max_x
    else:
        min_y = min(edge1[1], edge2[1])
        max_y = max(edge1[1], edge2[1])

        return p[0] == edge1[0] and min_y <= p[1] <= max_y

# Using ray casting algorithm by drawing a horizontal ray from the left:
# Source: https://stackoverflow.com/questions/217578/how-can-i-determine-whether-a-2d-point-is-within-a-polygon
def point_in_polygon(p, points):
    num_edges_hit = 0
    for idx in range(len(points)):
        edge_p = points[idx]
        edge_q = points[(idx+1) % len(points)]
        if point_in_edge(p, edge_p, edge_q):
            return True
        dir = get_edge_direction(edge_p, edge_q)
        if dir in "LR":
            if min(edge_p[0], edge_q[0]) > p[0] or p[1] != edge_p[1]:
                continue
            prev_dir = get_edge_direction(points[idx-1], edge_p)
            next_dir = get_edge_direction(edge_q, points[(idx+2) % len(points)])
            if prev_dir == next_dir:
                num_edges_hit += 1
        if edge_p[0] > p[0]:
            continue
        min_y = min(edge_p[1], edge_q[1])
        max_y = max(edge_p[1], edge_q[1])
        if min_y < p[1] < max_y:
            num_edges_hit += 1
    return num_edges_hit % 2 != 0

def get_path_direction(points):
    right_turns = 0
    left_turns = 0
    for idx in range(len(points)):
        dir1 = get_edge_direction(points[idx], points[(idx+1) % len(points)])
        dir2 = get_edge_direction(points[(idx+1) % len(points)], points[(idx+2) % len(points)])
        if (
            dir1 == "U" and dir2 == "R" or
            dir1 == "R" and dir2 == "D" or
            dir1 == "D" and dir2 == "L" or
            dir1 == "L" and dir2 == "U"
        ):
            right_turns += 1
        # elif (
        #     dir1 == "U" and dir2 == "L" or
        #     dir1 == "L" and dir2 == "D" or
        #     dir1 == "D" and dir2 == "R" or
        #     dir1 == "R" and dir2 == "U"
        # ):
        else:
            left_turns += 1
    if right_turns > left_turns:
        return "CW"
    # elif left_turns > right_turns:
    else:
        return "CCW"

def print_grid_with_details(edge1, edge2, corner1, corner2, points):
    def x(p):
        return p[0]
    def y(p):
        return p[1]
    points = list(map(lambda p: (p[0]//100, p[1]//100), points))
    if corner1 and corner2:
        min_x = min(corner1[0], corner2[0])
        max_x = max(corner1[0], corner2[0])
        min_y = min(corner1[1], corner2[1])
        max_y = max(corner1[1], corner2[1])
    for j in range(min(points, key=y)[1], max(points, key=y)[1]+1):
        for i in range(min(points, key=x)[0], max(points, key=x)[0]+1):
            if edge1 and edge2 and point_in_edge((i,j), edge1, edge2):
                dir = get_edge_direction(edge1, edge2) 
                if dir in "LR":
                    print("-", end="")
                else:
                    print("|", end="")
            elif corner1 and corner2 and min_x <= i <= max_x and min_y <= j <= max_y:
                print("O", end="")
            elif (i,j) in points:
                print("#", end="")
            elif point_in_polygon((i,j), points):
                print("X", end="")
            else:
                print(".", end="")
        print()

ans = 0
points = list()
min_x = 1000000
max_x = 0
min_y = 1000000
max_y = 0

for line in lines:
    x, y = line.split(",")
    points.append((int(x), int(y)))
    min_x = min(min_x, int(x))
    max_x = max(max_x, int(x))
    min_y = min(min_y, int(y))
    max_y = max(max_y, int(y))

# print_grid_with_details(None, None, None, None, points)
# print()
# print_grid_with_details((11,10), (11,3), (0,5), (15,10), points)

edges = list()
for idx in range(len(points)):
    p = points[idx]
    q = points[(idx+1) % len(points)]
    edges.append((p,q))

h_num = 0
v_num = 0
for edge1 in edges:
    for edge2 in edges:
        dir1 = get_edge_direction(edge1[0], edge1[1])
        dir2 = get_edge_direction(edge2[0], edge2[1])
        if dir1 != dir2:
            continue
        if dir1 in "LR":
            if edge1[0][1] == edge2[0][1] + 1:
                h_num += 1
        else:
            if edge1[0][0] == edge2[0][0] + 1:
                v_num += 1

print(h_num,v_num)

print(get_path_direction(points))

### THIS APPROACH DOESN'T WORK ###
# outside_points = set()
# next_points = set([(min_x,min_y)])
# while next_points:
#     p = next_points.pop()
#     outside_points.add(p)
#     for adj in [(p[0]+1,p[1]), (p[0]-1,p[1]), (p[0],p[1]+1), (p[0],p[1]-1)]:
#         if not (min_x-1 <= adj[0] <= max_x+1 and min_y-1 <= adj[1] <= max_y+1):
#             continue
#         if adj in outside_points:
#             continue
#         if any(map(lambda e: point_in_edge(adj, e[0], e[1]), edges)):
#             continue
#         next_points.add(adj)
#
# outside_points = set(filter(lambda p: min_x <= p[0] <= max_x and min_y <= p[1] <= max_y, outside_points))
# print(len(outside_points))
# print(outside_points)
### THIS APPROACH DOESN'T WORK ###

### THIS APPROACH ALMOST WORKS ###
for tile1 in tqdm(points):
    for tile2 in points:
        if tile1 == tile2:
            continue
        area = abs(tile1[0] - tile2[0] + 1) * abs(tile1[1] - tile2[1] + 1)
        if area < 1543467432:
            continue
        # if area <= ans:
        #     continue
        debug = False
        if area > ans:
            debug = True

        # Check if the rectangle is within the polygon defined by the red tiles
        # See https://stackoverflow.com/questions/4833802/check-if-polygon-is-inside-a-polygon
        invalid = False
        for idx in range(len(points)):
            # TODO: Figure out how to account for adjacent edges
            # Check if any edge of the polygon intersects with the rectangle
            p = points[idx]
            q = points[(idx+1) % len(points)]
            if edge_intersects_rect(p, q, tile1, tile2):
                if debug:
                    print(f"Rect {tile1} to {tile2} ({area}) invalid: Edge {p} -> {q} intersects")
                dir = get_edge_direction(p, q)
                min_x = min(tile1[0], tile2[0])
                max_x = max(tile1[0], tile2[0])
                min_y = min(tile1[1], tile2[1])
                max_y = max(tile1[1], tile2[1])
                if dir == "U":
                    for i in range(min_y, max_y):
                        for edge in edges:
                            if point_in_edge((p[0]-1, i), edge[0], edge[1]):
                                break
                        else:
                            invalid = True
                            break
                elif dir == "R":
                    for i in range(min_x, max_x):
                        for edge in edges:
                            if point_in_edge((i, p[1]-1), edge[0], edge[1]):
                                break
                        else:
                            invalid = True
                            break
                elif dir == "D":
                    for i in range(min_y, max_y):
                        for edge in edges:
                            if point_in_edge((p[0]+1, i), edge[0], edge[1]):
                                break
                        else:
                            invalid = True
                            break
                elif dir == "L":
                    for i in range(min_x, max_x):
                        for edge in edges:
                            if point_in_edge((i, p[1]+1), edge[0], edge[1]):
                                break
                        else:
                            invalid = True
                            break
                if invalid:
                    break
        if invalid:
            continue
        midpoint = ((tile1[0]+tile2[0])//2, (tile1[1]+tile2[1])//2)
        invalid = not point_in_polygon(midpoint, points)
        if invalid:
            if debug:
                print(f"Rect {tile1} to {tile2} invalid: Point {midpoint} not in polygon")
            continue

        if area > ans:
            print(f"New max area {area} from {tile1} to {tile2}")
            ans = area

print(ans)
### THIS APPROACH ALMOST WORKS ###
