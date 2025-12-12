"""
--- Advent of Code 2025 ---
--- Day 7:  ---
https://adventofcode.com/2025/day/7
"""

from time import perf_counter

TEST = False

DAY = "7"
REAL_INPUT = "Advent-of-Code-2025/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2025/Day" + DAY + "/input_test.txt"

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT

SOURCE = "S"
SPLITTER = "^"


def main():
    """Main program"""
    data = get_input_data(FILENAME)
    print(f"Tachyon Beam total split Part I {tachyon_beams(data)}")
    print(f"Tachyon Many Worlds Calcualtion Part II {tachyon_permutations(data)}")


def tachyon_beams(tachyon_manifold):
    """calculate the number of timees the tachyon beam is split"""
    source_location = tachyon_manifold[0].find(SOURCE)
    tachyon_beam_locations = {source_location}
    beam_split_count = 0
    for row in tachyon_manifold:
        for splitter in get_splitter_locations(row):
            if splitter in tachyon_beam_locations:
                beam_split_count += 1
            tachyon_beam_locations.discard(splitter)
            tachyon_beam_locations.add(splitter - 1)
            tachyon_beam_locations.add(splitter + 1)
    return beam_split_count


def tachyon_permutations(tachyon_manifold):
    """Calculate the number of paths a tachyon can take through the manifold"""
    source_location = tachyon_manifold[0].find(SOURCE)
    tachyon_path_count = {source_location: 1}
    total_beam_count = 0
    for row in tachyon_manifold:
        for splitter in get_splitter_locations(row):
            if splitter in tachyon_path_count:
                path_number = tachyon_path_count[splitter]
                del tachyon_path_count[splitter]
                if splitter - 1 in tachyon_path_count:
                    tachyon_path_count[splitter - 1] += path_number
                else:
                    tachyon_path_count[splitter - 1] = path_number
                if splitter + 1 in tachyon_path_count:
                    tachyon_path_count[splitter + 1] += path_number
                else:
                    tachyon_path_count[splitter + 1] = path_number
    for beam_paths in tachyon_path_count.values():
        total_beam_count += beam_paths
    return total_beam_count


def get_splitter_locations(manifold_row):
    """return a list of the positions of the splitters in the row"""
    splitter_locations = []
    for position in range(len(manifold_row)):
        if manifold_row[position] == SPLITTER:
            splitter_locations.append(position)
    return splitter_locations


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
