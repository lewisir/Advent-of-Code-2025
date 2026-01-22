"""
--- Advent of Code 2025 ---
--- Day 9:  ---
https://adventofcode.com/2025/day/9
"""

from time import perf_counter
from math import sqrt
from math import inf
from pprint import pprint

TEST = True

DAY = "9"
REAL_INPUT = "Advent-of-Code-2025/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2025/Day" + DAY + "/input_test.txt"

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT

DIRECTIONS = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}
TURNS = {
    ((0, -1), (1, 0)): "R",
    ((1, 0), (0, 1)): "R",
    ((0, 1), (-1, 0)): "R",
    ((-1, 0), (0, -1)): "R",
    ((0, -1), (-1, 0)): "L",
    ((-1, 0), (0, 1)): "L",
    ((0, 1), (1, 0)): "L",
    ((1, 0), (0, -1)): "L",
}
SIDES = {
    (0, -1): {"L": (-1, 0), "R": (1, 0)},
    (1, 0): {"L": (0, -1), "R": (0, 1)},
    (0, 1): {"L": (1, 0), "R": (-1, 0)},
    (-1, 0): {"L": (0, 1), "R": (0, -1)},
}


def main():
    """Main program"""
    data = get_input_data(FILENAME)
    red_tile_locations = process(data)
    print(f"Largest Rectangle Area Part I {find_largest_rectangle(red_tile_locations)}")
    print(f"Part II - vectorising perimeter {perf_counter() - start_time}")
    vector_perimeter = vectorise_perimeter(red_tile_locations)
    # print(f"start at {red_tile_locations[-1]}")
    # print(f"{vector_perimeter}")
    print(f"Part II - determiniing perimeter points {perf_counter() - start_time}")
    perm_points = perimeter_points(red_tile_locations[-1], vector_perimeter)
    print(
        f"Part II - identifying adjacent internal points {perf_counter() - start_time}"
    )
    adj_ext_points = record_adjacent_points(red_tile_locations[-1], vector_perimeter)
    adj_ext_points.difference_update(perm_points)
    adj_ext_points.difference_update(red_tile_locations)
    print(f"Part II - number of adjacent points {len(adj_ext_points)}")
    display_tiles(red_tile_locations, adj_ext_points)
    print(
        f"Largest Rectangle Area Part II {find_largest_conforming_rectangle(red_tile_locations, adj_ext_points)}"
    )
    # 1568814424 was found in 450 seconds and is wrong and too low!


def find_largest_rectangle(red_tile_locations):
    """Find the largest rectangle that can be formed by any two red tiles (part I)"""
    largest_area = 0
    for rtl1 in red_tile_locations:
        for rtl2 in red_tile_locations:
            area = rectangle_size(rtl1, rtl2)
            if area > largest_area:
                largest_area = area
    return largest_area


def find_largest_conforming_rectangle(red_tile_locations, adj_ext_points):
    """find the largest rectangle that can be formed by any two red tiles and is within the shape (part II)"""
    largest_area = 0
    for rtl1 in red_tile_locations:
        for rtl2 in red_tile_locations:
            if rtl1 != rtl2:
                if conforming_rectangle(rtl1, rtl2, adj_ext_points):
                    area = rectangle_size(rtl1, rtl2)
                    if area > largest_area:
                        largest_area = area
    return largest_area


def conforming_rectangle(rtl1, rtl2, adj_ext_points):
    """Check whether there are any external points within the rectangle and return True if not"""
    x1, y1 = rtl1
    x2, y2 = rtl2
    x_min = min(x1, x2)
    x_max = max(x1, x2)
    y_min = min(y1, y2)
    y_max = max(y1, y2)
    for point in adj_ext_points:
        x, y = point
        if x >= x_min and x <= x_max and y >= y_min and y <= y_max:
            return False
    return True


def rectangle_size(corner1, corner2):
    """return the area of the rectangle defines by the two corners"""
    return abs(corner1[0] - corner2[0] + 1) * abs(corner1[1] - corner2[1] + 1)


def vectorise_perimeter(red_tile_locations):
    """Produce a list of vectors that will trace out the perimeter starting at the last point in the list of red tiles"""
    vector_perimeter = []
    rtl2 = red_tile_locations[-1]
    for rtl1 in red_tile_locations:
        vector_perimeter.append(displacement_vector(rtl1, rtl2))
        rtl2 = rtl1
    return vector_perimeter


def analyse_perimeter(vector_perimeter):
    """Return some stats about the perimeter"""
    max_x, max_y = 0, 0
    min_x, min_y = inf, inf
    for vector in vector_perimeter:
        x, y = vector
        if min_x == None:
            min_x = x
        if max_x == None:
            max_x = x
        if min_y == None:
            min_y = y
        if max_y == None:
            max_y = y
        if x != 0 and abs(x) < min_x:
            min_x = abs(x)
        if y != 0 and abs(y) < min_y:
            min_y = abs(y)
        if abs(x) > max_x:
            max_x = abs(x)
        if abs(y) > max_y:
            max_y = abs(y)
    return min_x, max_x, min_y, max_y


def perimeter_points(position, vector_perimeter):
    """Return all the points that make up the perimeter"""
    perimeter_points = set()
    for vector in vector_perimeter:
        vector_comps = vector_components(vector)
        perimeter_points.update(line_points(position, vector_comps))
        position = add_vectors(position, vector)
    return perimeter_points


def line_points(position, vector_components):
    """from the starting position follow the vector and return the set of points"""
    points = set()
    x, y = position
    magnitude = vector_components["magnitude"]
    dx, dy = vector_components["direction"]
    for m in range(magnitude):
        points.add((x + m * dx, y + m * dy))
    return points


def rotation_direction(vector_perimeter):
    """Following the perimeter return whether the outside of the shaper is to the Left or Right of the perimeter"""
    l_count, r_count = 0, 0
    direction = vector_components(vector_perimeter[-1])["direction"]
    for vector in vector_perimeter:
        turn = compare_vector_dir(direction, vector_components(vector)["direction"])
        direction = vector_components(vector)["direction"]
        if turn == "L":
            l_count += 1
        else:
            r_count += 1
    if l_count > r_count:
        inside = "L"
        outside = "R"
    else:
        inside = "R"
        outside = "L"
    return outside


def record_adjacent_points(position, vector_perimeter):
    """Return the set of points that are adjacent to the perimeter. Inside or Outside is controlled by the rotation_direction"""
    side = rotation_direction(vector_perimeter)
    adjacent_points = set()
    last_vector = None
    for vector in vector_perimeter:
        vector_comps = vector_components(vector)
        adjacent_points.update(line_adj_points(position, vector_comps, side))
        if (
            last_vector is not None
            and compare_vector_dir(
                vector_components(last_vector)["direction"], vector_comps["direction"]
            )
            != side
        ):
            # add the extra internal point that is to the side and behind the position
            adjacent_points.add(corner_point(position, vector_comps, side))
        last_vector = vector
        position = add_vectors(position, vector)
    # Run a final vector to handle the turn back to the starting vector
    vector_comps = vector_components(vector_perimeter[0])
    if (
        compare_vector_dir(
            vector_components(last_vector)["direction"], vector_comps["direction"]
        )
        != side
    ):
        # add the extra internal point that is to the side and behind the position
        adjacent_points.add(corner_point(position, vector_comps, side))
    return adjacent_points


def line_adj_points(position, vector_comps, side):
    """return the set of points adjacent to the line"""
    points = set()
    x, y = position
    magnitude = vector_comps["magnitude"]
    dx, dy = vector_comps["direction"]
    adj_x = SIDES[vector_comps["direction"]][side][0]
    adj_y = SIDES[vector_comps["direction"]][side][1]
    for m in range(magnitude + 1):
        points.add((x + adj_x + m * dx, y + adj_y + m * dy))
    return points


def corner_point(position, vector_comps, side):
    """return the extra point when the perimeter that is to the side and 'behind' the position"""
    x, y = position
    dx, dy = vector_comps["direction"]
    adj_x = SIDES[vector_comps["direction"]][side][0]
    adj_y = SIDES[vector_comps["direction"]][side][1]
    behind_x, behind_y = 0, 0
    if dy != 0:
        behind_y = -1 * dy
    elif dx != 0:
        behind_x = -1 * dx
    return (x + adj_x + behind_x, y + adj_y + behind_y)


def search_internal_points(position, all_points):
    """find all the points within the shape, from the position"""
    next_points = get_valid_neighbours(position, all_points)
    while len(next_points) > 0:
        position = next_points.pop()
        all_points.add(position)
        next_points.extend(get_valid_neighbours(position, all_points))
    return all_points


def get_valid_neighbours(position, all_points):
    """from the position return a list of the valid neighbours (those that are not already in all_points)"""
    neighbours = []
    for direction in DIRECTIONS.values():
        new_position = add_vectors(position, direction)
        if new_position not in all_points:
            neighbours.append(new_position)
    return neighbours


def rectangle_points(corner1, corner2):
    """Return the set of points that are in the rectangle defined by the two corners"""
    rect_points = set()
    minx = min(corner1[0], corner2[0])
    miny = min(corner1[1], corner2[1])
    maxx = max(corner1[0], corner2[0])
    maxy = max(corner1[1], corner2[1])
    for x in range(minx, maxx + 1):
        for y in range(miny, maxy + 1):
            rect_points.add((x, y))
    return rect_points


def displacement_vector(point1, point2):
    """Return the vector tuple that will give the position of point2 from the point of view of point1"""
    return point1[0] - point2[0], point1[1] - point2[1]


def add_vectors(point1, vector):
    """Add the vector to the point to get a new point"""
    return point1[0] + vector[0], point1[1] + vector[1]


def compare_vector_dir(vector1, vector2):
    """Return the direction of the turn either 'L' or 'R"""
    return TURNS[(vector1, vector2)]


def create_vector(vector_components):
    """return the vector formed by the components"""
    mag = vector_components["magnitude"]
    dir = vector_components["direction"]
    x, y = dir
    return (mag * x, mag * y)


def vector_components(vector):
    """Given the vector return the magnitude and directional unit vector"""
    vector_comps = {}
    x, y = vector
    vector_comps["magnitude"] = max(abs(x), abs(y))
    if x > 0:
        unit = (1, 0)
    elif x < 0:
        unit = (-1, 0)
    elif y > 0:
        unit = (0, 1)
    elif y < 0:
        unit = (0, -1)
    else:
        unit = (0, 0)
    vector_comps["direction"] = unit
    return vector_comps


def display_tiles(red_tiles, green_tiles):
    """print out the tiles"""
    max_x, max_y = 0, 0
    for tile in red_tiles:
        if tile[0] > max_x:
            max_x = tile[0]
        if tile[1] > max_y:
            max_y = tile[1]
    tile_map = [["." for x in range(max_x + 2)] for y in range(max_y + 2)]
    for tile in green_tiles:
        x, y = tile
        tile_map[y][x] = "O"
    for tile in red_tiles:
        x, y = tile
        tile_map[y][x] = "#"
    output_map = ["".join(x) for x in tile_map]
    for line in output_map:
        print(line)


def process(data):
    """Process the data to return a list ot tuples with each tuple recording the location of the red tiles"""
    red_tile_locations = []
    for line in data:
        red_tile_locations.append(tuple([int(x) for x in line.split(",")]))
    return red_tile_locations


def get_input_data(filename):
    """function to read in the input data"""
    file_data = []
    with open(filename) as file:
        for line in file:
            file_data.append(line.rstrip("\n"))
    return file_data


if __name__ == "__main__":
    start_time = perf_counter()
    main()
    print(f"-- Time Taken {perf_counter() - start_time}")
