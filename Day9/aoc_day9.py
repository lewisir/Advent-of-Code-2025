"""
--- Advent of Code 2025 ---
--- Day 9:  ---
https://adventofcode.com/2025/day/9
"""

from time import perf_counter
from math import sqrt
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
    vector_perimeter = vectorise_perimeter(red_tile_locations)
    print(vector_perimeter)
    print(rotation_direction(vector_perimeter))
    # print(
    #    record_adjacent_internal_points(
    #        red_tile_locations[-1], vector_perimeter
    #    )
    # )
    # print(line_adj_points((4, 4), {"magnitude": 3, "direction": (1, 0)}, "L"))
    green_tile_locations = record_adjacent_internal_points(
        red_tile_locations[-1], vector_perimeter
    )
    display_tiles(red_tile_locations, green_tile_locations)


def find_largest_rectangle(red_tile_locations):
    """Find the largest rectangle that can be formed by any two red tiles (part I)"""
    largest_area = 0
    for rtl1 in red_tile_locations:
        for rtl2 in red_tile_locations:
            area = rectangle_size(rtl1, rtl2)
            if area > largest_area:
                largest_area = area
    return largest_area


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
    """Following the perimeter return whether the perimeter is passed in a clockwise (R) or anti-clockwise (R) direction"""
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
        return "L"
    else:
        return "R"


def record_adjacent_internal_points(position, vector_perimeter):
    """Return the set of points that are inside and adjacent to the perimeter"""
    inside = rotation_direction(vector_perimeter)
    adjacent_points = set()
    for vector in vector_perimeter:
        vector_comps = vector_components(vector)
        adjacent_points.update(line_adj_points(position, vector_comps, inside))
        position = add_vectors(position, vector)
    return adjacent_points


def line_adj_points(position, vector_comps, inside):
    """return the set of points adjacent to the line"""
    points = set()
    x, y = position
    magnitude = vector_comps["magnitude"]
    dx, dy = vector_comps["direction"]
    adj_x = SIDES[vector_comps["direction"]][inside][0]
    adj_y = SIDES[vector_comps["direction"]][inside][1]
    for m in range(magnitude):
        points.add((x + adj_x + m * dx, y + adj_y + m * dy))
    return points


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
    tile_line = ["." for x in range(max_x + 1)]
    tile_map = [tile_line for y in range(max_y + 1)]
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
