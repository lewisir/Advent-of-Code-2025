"""
--- Advent of Code 2025 ---
--- Day 4:  ---
https://adventofcode.com/2025/day/4
"""

from time import perf_counter

TEST = True

DAY = "4"
REAL_INPUT = "Advent-of-Code-2025/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2025/Day" + DAY + "/input_test.txt"

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT

ADJACENT_DIRECTIONS = {
    1: (-1, -1),
    2: (-1, 0),
    3: (-1, 1),
    4: (0, -1),
    6: (0, 1),
    7: (1, -1),
    8: (1, 0),
    9: (1, 1),
}


def main():
    """Main program"""
    data = get_input_data(FILENAME)
    paper_map = process_data(data)
    print(f"Part I accessible rolls {count_accessible_rolls(paper_map)}")
    print(f"Part II accessible rolls {repeat_removals(paper_map)}")


def repeat_removals(paper_map):
    """Repeat the removal of roll removed no more can be removed"""
    total_roll_count = 0
    available_rolls = 1
    while available_rolls > 0:
        available_rolls = count_accessible_rolls(paper_map, True)
        total_roll_count += available_rolls
    return total_roll_count


def count_accessible_rolls(paper_map, mark_removal=False):
    """Work through the map counting the number of positions where rolls are that have fewer than four adjacent rolls"""
    accessible_roll_count = 0
    for y, row in enumerate(paper_map):
        for x, cell in enumerate(row):
            if cell == "@":
                if count_adjacent_rolls(paper_map, (y, x)) < 4:
                    accessible_roll_count += 1
                    if mark_removal:
                        paper_map[y][x] = "x"
    return accessible_roll_count


def count_adjacent_rolls(paper_map, position):
    """return the number of rolls adjacent to the position"""
    roll_count = 0
    for adj_position in get_adjacent_positions(
        position, len(paper_map), len(paper_map[0])
    ):
        y, x = adj_position
        if paper_map[y][x] == "@":
            roll_count += 1
    return roll_count


def get_adjacent_positions(start_position, map_max_y, map_max_x):
    """return a list of the positions adjacent (horizontal, vertical and diagonal) to the start_position"""
    adjacent_positions = []
    for direction in ADJACENT_DIRECTIONS:
        new_y = start_position[0] + ADJACENT_DIRECTIONS[direction][0]
        new_x = start_position[1] + ADJACENT_DIRECTIONS[direction][1]
        if new_y >= 0 and new_y < map_max_y and new_x >= 0 and new_x < map_max_x:
            adjacent_positions.append((new_y, new_x))
    return adjacent_positions


def display_map(paper_map):
    """Display the map"""
    for row in paper_map:
        print("".join(row))


def process_data(data):
    """process the data and return a 2D map"""
    paper_map = []
    for line in data:
        paper_map.append(list(line))
    return paper_map


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
