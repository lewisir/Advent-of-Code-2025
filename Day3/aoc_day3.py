"""
--- Advent of Code 2025 ---
--- Day 3:  ---
https://adventofcode.com/2025/day/3
"""

from time import perf_counter

TEST = False

DAY = "3"
REAL_INPUT = "Advent-of-Code-2025/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2025/Day" + DAY + "/input_test.txt"

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT


def main():
    """Main program"""
    data = get_input_data(FILENAME)
    print(f"Part I highest Joltage sum {process_battery_banks(data,2)}")
    print(f"Part II highest Joltage sum {process_battery_banks(data,12)}")


def process_battery_banks(data, size):
    """Process all the battery banks and return the sum of joltages"""
    joltage_sum = 0
    for bank in data:
        joltage_sum += find_highest_joltage(bank, size)
    return joltage_sum


def find_highest_joltage(battery_bank, size):
    """using the size of the number of batteries that can be include, find the highest joltage"""
    battery_positions = []
    while len(battery_positions) < size:
        if len(battery_positions) == 0:
            start_position = 0
        else:
            start_position = battery_positions[-1] + 1
        end_position = len(battery_bank) - size + len(battery_positions) + 1
        digit_position = (
            high_number_position(battery_bank[start_position:end_position])
            + start_position
        )
        battery_positions.append(digit_position)
    return combine_batteries(battery_bank, battery_positions)


def combine_batteries(battery_bank, positions):
    """Combine the batteries at the specified positions and return the joltage"""
    battery_list = []
    for battery in positions:
        battery_list.append(battery_bank[battery])
    joltage = int("".join(battery_list))
    return joltage


def high_number_position(digit_string):
    """return the position of the highest number in the digit string"""
    for number in range(9, -1, -1):
        for index, value in enumerate(digit_string):
            if value == str(number):
                return index


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
