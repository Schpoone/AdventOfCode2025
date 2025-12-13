from tqdm import tqdm
from typing import Literal

filename = "example1.txt"
# filename = "example2.txt"
filename = "input.txt"

lines = None
with open(filename, "r") as f:
    lines = f.readlines()

Point = tuple[int, int]
Edge = tuple[Point, Point]
Direction = Literal["U", "D", "L", "R"]
PathDirection = Literal["CW", "CCW"]

### Part 1 was trivial so it is NOT included here ###

def get_edge_direction(p: Point, q: Point) -> Direction:
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

def get_bounds(p: Point, q: Point) -> tuple[int, int, int, int]:
    min_x = min(p[0], q[0])
    max_x = max(p[0], q[0])
    min_y = min(p[1], q[1])
    max_y = max(p[1], q[1])
    return min_x, max_x, min_y, max_y

def edge_intersects_rect(edge1: Point, edge2: Point, corner1: Point, corner2: Point) -> bool:
    edge_min_x, edge_max_x, edge_min_y, edge_max_y = get_bounds(edge1, edge2)
    rect_min_x, rect_max_x, rect_min_y, rect_max_y = get_bounds(corner1, corner2)
    dir = get_edge_direction(edge1, edge2)
    if dir in "LR":
        edge_y = edge1[1]
        return rect_min_y < edge_y < rect_max_y and edge_max_x > rect_min_x and edge_min_x < rect_max_x
    else:
        edge_x = edge1[0]
        return rect_min_x < edge_x < rect_max_x and edge_max_y > rect_min_y and edge_min_y < rect_max_y

def point_in_edge(p: Point, edge1: Point, edge2: Point) -> bool:
    min_x, max_x, min_y, max_y = get_bounds(edge1, edge2)
    dir = get_edge_direction(edge1, edge2)
    if dir in "LR":
        return p[1] == edge1[1] and min_x <= p[0] <= max_x
    else:
        return p[0] == edge1[0] and min_y <= p[1] <= max_y

def get_path_direction(edges: list[Edge]) -> PathDirection:
    right_turns = 0
    left_turns = 0
    for idx in range(len(edges)):
        edge1 = edges[idx]
        edge2 = edges[(idx+1) % len(edges)]
        dir1 = get_edge_direction(edge1[0], edge1[1])
        dir2 = get_edge_direction(edge2[0], edge2[1])
        if (
            dir1 == "U" and dir2 == "R" or
            dir1 == "R" and dir2 == "D" or
            dir1 == "D" and dir2 == "L" or
            dir1 == "L" and dir2 == "U"
        ):
            right_turns += 1
        else:
            left_turns += 1
    if right_turns > left_turns:
        return "CW"
    else:
        return "CCW"

def is_edge_covered(p: Point, q: Point, corner1: Point, corner2: Point) -> bool:
    """Check if the outside tiles introduced by the intersecting edge is covered by other edges

    If there are many edges parallel and adjacent to each other,
    an edge can intersect in the middle of a rectangle
    but it's valid because its outside region is covered with edges

    Turns out, this doesn't happen in the input, so you can remove it
    to run much faster
    """
    global edges
    return False
    min_x, max_x, min_y, max_y = get_bounds(corner1, corner2)
    dir = get_edge_direction(p, q)
    path_dir = get_path_direction(edges)
    edge_range, outside_range = range(0), range(0)
    if dir == "U" and path_dir == "CW" or dir == "D" and path_dir == "CCW":
        edge_range = range(min_y, max_y)
        outside_range = range(min_x, p[0])
    elif dir == "R" and path_dir == "CW" or dir == "L" and path_dir == "CCW":
        edge_range = range(min_x, max_x)
        outside_range = range(min_y, p[1])
    elif dir == "D" and path_dir == "CW" or dir == "U" and path_dir == "CCW":
        edge_range = range(min_y, max_y)
        outside_range = range(p[0], max_x)
    elif dir == "L" and path_dir == "CW" or dir == "R" and path_dir == "CCW":
        edge_range = range(min_x, max_x)
        outside_range = range(p[1], max_y)

    for i in outside_range:
        for j in edge_range:
            if dir in "UD":
                p = (i, j)
            else:
                p = (j, i)
            for edge in edges:
                if point_in_edge(p, edge[0], edge[1]):
                    break
            else:
                return False
    return True

def point_in_polygon(p: Point, edges: list[Edge]):
    """Check if a point is in the polygon defined by edges

    Uses the ray casting algorithm by drawing a horizontal ray from the left
    See https://stackoverflow.com/questions/217578/how-can-i-determine-whether-a-2d-point-is-within-a-polygon
    """
    num_edges_hit = 0
    for idx in range(len(edges)):
        edge_p, edge_q = edges[idx]
        if point_in_edge(p, edge_p, edge_q):
            return True
        dir = get_edge_direction(edge_p, edge_q)
        if dir in "LR":
            if min(edge_p[0], edge_q[0]) > p[0] or p[1] != edge_p[1]:
                continue
            prev_edge = edges[idx-1]
            next_edge = edges[(idx+1) % len(edges)]
            prev_dir = get_edge_direction(prev_edge[0], prev_edge[1])
            next_dir = get_edge_direction(next_edge[0], next_edge[1])
            if prev_dir == next_dir:
                num_edges_hit += 1
        if edge_p[0] > p[0]:
            continue
        min_y = min(edge_p[1], edge_q[1])
        max_y = max(edge_p[1], edge_q[1])
        if min_y < p[1] < max_y:
            num_edges_hit += 1
    return num_edges_hit % 2 != 0

def is_rectangle_valid(corner1: Point, corner2: Point, edges: list[Edge], last_invalid_edge: Edge | None = None):
    """Check if the rectangle is within the polygon defined by points

    The rectangle is fully within the polygon if no edge of the polygon intersects
    with the rectangle and a point in the rectangle is in the polygon

    See https://stackoverflow.com/questions/4833802/check-if-polygon-is-inside-a-polygon

    This also optionally takes an edge to check first. The idea is to check the
    edge that caused the previous rectangle to fail because it is more likely
    to cause the current rectangle to fail as well.
    """
    for edge in [last_invalid_edge] + list(edges):
        if not edge:
            continue
        if edge_intersects_rect(edge[0], edge[1], corner1, corner2) and not is_edge_covered(edge[0], edge[1], corner1, corner2):
            return False, edge

    midpoint = ((corner1[0]+corner2[0])//2, (corner1[1]+corner2[1])//2)
    return point_in_polygon(midpoint, edges), None

def print_grid_with_details(edge: Edge | None = None, rect: Edge | None = None):
    global points, edges
    def x(p):
        return p[0]
    def y(p):
        return p[1]
    points = list(map(lambda p: (p[0]//100, p[1]//100), points))
    min_x = max_x = min_y = max_y = 0
    if rect:
        min_x, max_x, min_y, max_y = get_bounds(rect[0], rect[1])
    for j in range(min(points, key=y)[1], max(points, key=y)[1]+1):
        for i in range(min(points, key=x)[0], max(points, key=x)[0]+1):
            if edge and point_in_edge((i,j), edge[0], edge[1]):
                dir = get_edge_direction(edge[0], edge[1]) 
                if dir in "LR":
                    print("-", end="")
                else:
                    print("|", end="")
            elif rect and min_x <= i <= max_x and min_y <= j <= max_y:
                print("O", end="")
            elif (i,j) in points:
                print("#", end="")
            elif point_in_polygon((i,j), edges):
                print("X", end="")
            else:
                print(".", end="")
        print()

ans = 0
points = list()

for line in lines:
    x, y = line.split(",")
    points.append((int(x), int(y)))

# print_grid_with_details()
# print()
# print_grid_with_details(((11,10), (11,3)), ()(0,5), (15,10)))

edges = list()
for idx in range(len(points)):
    p = points[idx]
    q = points[(idx+1) % len(points)]
    edges.append((p,q))

last_invalid_edge = None
for tile1 in tqdm(points):
    for tile2 in points:
        if tile1 == tile2:
            continue
        area = (abs(tile1[0] - tile2[0]) + 1) * (abs(tile1[1] - tile2[1]) + 1)
        if area <= ans:
            continue
        valid, last_invalid_edge = is_rectangle_valid(tile1, tile2, edges, last_invalid_edge)
        if not valid:
            continue
        if area > ans:
            tqdm.write(f"New max area {area} from {tile1} to {tile2}")
            ans = area

print(ans)
