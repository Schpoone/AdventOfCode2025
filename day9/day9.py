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

def get_bounds(p, q):
    min_x = min(p[0], q[0])
    max_x = max(p[0], q[0])
    min_y = min(p[1], q[1])
    max_y = max(p[1], q[1])
    return min_x, max_x, min_y, max_y

def edge_intersects_rect(edge1, edge2, corner1, corner2):
    edge_min_x, edge_max_x, edge_min_y, edge_max_y = get_bounds(edge1, edge2)
    rect_min_x, rect_max_x, rect_min_y, rect_max_y = get_bounds(corner1, corner2)
    dir = get_edge_direction(edge1, edge2)
    if dir in "LR":
        edge_y = edge1[1]
        return rect_min_y < edge_y < rect_max_y and edge_max_x > rect_min_x and edge_min_x < rect_max_x
    elif dir in "UD":
        edge_x = edge1[0]
        return rect_min_x < edge_x < rect_max_x and edge_max_y > rect_min_y and edge_min_y < rect_max_y

def point_in_edge(p, edge1, edge2):
    min_x, max_x, min_y, max_y = get_bounds(edge1, edge2)
    dir = get_edge_direction(edge1, edge2)
    if dir in "LR":
        return p[1] == edge1[1] and min_x <= p[0] <= max_x
    else:
        return p[0] == edge1[0] and min_y <= p[1] <= max_y

def point_in_polygon(p, points):
    """Check if a point is in the polygon defined by points

    Uses the ray casting algorithm by drawing a horizontal ray from the left
    See https://stackoverflow.com/questions/217578/how-can-i-determine-whether-a-2d-point-is-within-a-polygon
    """
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

def is_rectangle_valid(corner1, corner2, points):
    """Check if the rectangle is within the polygon defined by points

    The rectangle is fully within the polygon if no edge of the polygon intersects
    with the rectangle and a point in the rectangle is in the polygon

    See https://stackoverflow.com/questions/4833802/check-if-polygon-is-inside-a-polygon
    """
    for idx in range(len(points)):
        p = points[idx]
        q = points[(idx+1) % len(points)]
        if edge_intersects_rect(p, q, corner1, corner2):
            # If there are many edges parallel and adjacent to each other,
            # an edge can intersect in the middle of a rectangle
            # but it's valid because its outside region is covered with edges
            # Turns out, this doesn't happen in the input, so you can remove it
            # to run much faster
            min_x, max_x, min_y, max_y = get_bounds(corner1, corner2)
            dir = get_edge_direction(p, q)
            if dir == "U":
                for i in range(min_y, max_y):
                    for edge in edges:
                        if point_in_edge((p[0]-1, i), edge[0], edge[1]):
                            break
                    else:
                        return False
            elif dir == "R":
                for i in range(min_x, max_x):
                    for edge in edges:
                        if point_in_edge((i, p[1]-1), edge[0], edge[1]):
                            break
                    else:
                        return False
            elif dir == "D":
                for i in range(min_y, max_y):
                    for edge in edges:
                        if point_in_edge((p[0]+1, i), edge[0], edge[1]):
                            break
                    else:
                        return False
            elif dir == "L":
                for i in range(min_x, max_x):
                    for edge in edges:
                        if point_in_edge((i, p[1]+1), edge[0], edge[1]):
                            break
                    else:
                        return False

    midpoint = ((corner1[0]+corner2[0])//2, (corner1[1]+corner2[1])//2)
    return point_in_polygon(midpoint, points)

def print_grid_with_details(edge1, edge2, corner1, corner2, points):
    def x(p):
        return p[0]
    def y(p):
        return p[1]
    points = list(map(lambda p: (p[0]//100, p[1]//100), points))
    if corner1 and corner2:
        min_x, max_x, min_y, max_y = get_bounds(corner1, corner2)
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

for line in lines:
    x, y = line.split(",")
    points.append((int(x), int(y)))

# print_grid_with_details(None, None, None, None, points)
# print()
# print_grid_with_details((11,10), (11,3), (0,5), (15,10), points)

edges = list()
for idx in range(len(points)):
    p = points[idx]
    q = points[(idx+1) % len(points)]
    edges.append((p,q))

for tile1 in tqdm(points):
    for tile2 in points:
        if tile1 == tile2:
            continue
        area = (abs(tile1[0] - tile2[0]) + 1) * (abs(tile1[1] - tile2[1]) + 1)
        if area <= ans:
            continue
        if not is_rectangle_valid(tile1, tile2, points):
            continue
        if area > ans:
            print(f"New max area {area} from {tile1} to {tile2}")
            ans = area

print(ans)
