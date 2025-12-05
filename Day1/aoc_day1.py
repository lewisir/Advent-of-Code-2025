"""
--- Advent of Code 2025 ---
--- Day 1:  ---
https://adventofcode.com/2025/day/11
"""

from time import perf_counter

TEST = False

DAY = "1"
REAL_INPUT = "Advent-of-Code-2025/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2025/Day" + DAY + "/input_test.txt"

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT

START_NUMBER = 50
TOTAL_DIAL_NUMBER = 100
TESTS = [
    ["L49"],  # from non-zero rotate Left and do not pass 0 - zero-count = 0
    ["L50"],  # from non-zero rotate Left and land on 0 - zero-count = 1
    ["L51"],  # from non-zero rotate Left pass 0 once - zero-count = 1
    ["R49"],  # from non-zero rotate Right and do not pass 0 - zero-count = 0
    ["R50"],  # from non-zero rotate Right and land on 0 - zero-count = 1
    ["R51"],  # from non-zero rotate Right pass 0 once - zero-count = 1
    ["L149"],  # from non-zero rotate Left and do not pass 1 - zero-count = 1
    [
        "L150"
    ],  # from non-zero rotate Left and pass zero once and then land on 0 - zero-count = 2
    ["L151"],  # from non-zero rotate Left pass 0 twice - zero-count = 2
    ["R149"],  # from non-zero rotate Right and do not pass 1 - zero-count = 1
    [
        "R150"
    ],  # from non-zero rotate Right and pass zero once and then land on 0 - zero-count = 2
    ["R151"],  # from non-zero rotate Right pass 0 twice - zero-count = 2
    ["L50", "L99"],  # from zero rotate Left and do not pass 0
    ["R50", "R1"],  # from zero rotate Right and do not pass 0
    ["L50", "L100"],  # from zero rotate Left and land on 0
    ["R50", "R100"],  # from zero rotate Right and land on 0
    ["L50", "L101"],  # from zero rotate Left and pass 0 once finishing on non-zero
    ["R50", "R199"],  # from zero rotate Right and pass 0 once finishing on non-zero
    ["L50", "L299"],  # from zero rotate Left and pass 0 twice finishing on non-zero
    ["R50", "R201"],  # from zero rotate Right and pass 0 twice finishing on non-zero
    ["L50", "L200"],  # from zero rotate Left and land on 0 passing through 0 once
    ["R50", "R200"],  # from zero rotate Right and land on 0 passing through 0 once
    ["L50", "L300"],  # from zero rotate Left and land on 0 passing through 0 twice
    ["R50", "R300"],  # from zero rotate Right and land on 0 passing through 0 twice
]


def main():
    """Main program"""
    data = get_input_data(FILENAME)
    print(f"Part I Password is {process_rotations_part_i(data)}")
    # print(f"Part II Password is {process_rotations_part_ii(data)}")
    print(f"Part II Password is {process_rotations_brute(data)}")
    # for test in TESTS:
    #    print(f"Test: {test}\nResult:{process_rotations_part_ii(test)}")


def process_rotations_part_i(input_rotations):
    """process each rotation and return how many times the dial points at zero"""
    zero_counter = 0
    dial_number = START_NUMBER
    for rotation in input_rotations:
        direction, distance = extract_rotation(rotation)
        if direction == "L":
            dial_number -= distance
        elif direction == "R":
            dial_number += distance
        dial_number = dial_number % TOTAL_DIAL_NUMBER
        if dial_number == 0:
            zero_counter += 1
    return zero_counter


def process_rotations_part_ii(input_rotations):
    """process each rotation and return how many times the dial points to or passes zero"""
    # The maths here are not right!
    zero_counter = 0
    dial_number = START_NUMBER
    for rotation in input_rotations:
        direction, distance = extract_rotation(rotation)
        if dial_number == 0:
            zero_counter += distance // TOTAL_DIAL_NUMBER
            if distance % TOTAL_DIAL_NUMBER == 0:
                continue
            elif direction == "L":
                dial_number -= distance
            elif direction == "R":
                dial_number += distance
        else:
            if direction == "L":
                if distance > dial_number:
                    zero_counter += (
                        TOTAL_DIAL_NUMBER + distance - dial_number
                    ) // TOTAL_DIAL_NUMBER
                dial_number -= distance
            elif direction == "R":
                if distance > TOTAL_DIAL_NUMBER - dial_number:
                    zero_counter += (distance + dial_number) // TOTAL_DIAL_NUMBER
                dial_number += distance
        dial_number = dial_number % TOTAL_DIAL_NUMBER
        if dial_number == 0:
            zero_counter += 1
    return zero_counter


def process_rotations_brute(input_rotations):
    """Brute for the rotations"""
    zero_counter = 0
    dial_number = START_NUMBER
    for rotation in input_rotations:
        direction, distance = extract_rotation(rotation)
        if direction == "L":
            turn = -1
        else:
            turn = 1
        for _ in range(distance):
            dial_number += turn
            if dial_number == 0 or dial_number == 100:
                zero_counter += 1
            dial_number = dial_number % TOTAL_DIAL_NUMBER
    return zero_counter


def extract_rotation(rotation):
    """From the input string extract the direction (L or R) and the distance"""
    direction = rotation[0]
    distance = int(rotation[1:])
    return direction, distance


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
