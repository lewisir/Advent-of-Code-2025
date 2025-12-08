"""
--- Advent of Code 2025 ---
--- Day 2:  ---
https://adventofcode.com/2025/day/2
"""

from time import perf_counter

TEST = False

DAY = "2"
REAL_INPUT = "Advent-of-Code-2025/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2025/Day" + DAY + "/input_test.txt"

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT


def main():
    """Main program"""
    data = get_input_data(FILENAME)
    data = extract_input_id_ranges(data[0])
    print(f"Invalid ID total part I {process_ranges_i(data)}")
    print(f"Invalid ID total part II {process_ranges_ii(data)}")


def process_ranges_i(data):
    """Work through each range and sum the invalid IDs using part I definition of invalid"""
    invalid_id_sum = 0
    for id_range in data:
        invalid_id_sum += sum_invalid_ids_i(id_range)
    return invalid_id_sum


def process_ranges_ii(data):
    """Work through each range and sum the invalid IDs using part II definition of invalid"""
    invalid_id_sum = 0
    for id_range in data:
        invalid_id_sum += sum_invalid_ids_ii(id_range)
    return invalid_id_sum


def sum_invalid_ids_i(input_range):
    """return a sum of the invalid IDs found in the range"""
    fist_id = int(input_range.split("-")[0])
    last_id = int(input_range.split("-")[1])
    product_id = fist_id
    invalid_id_sum = 0
    while product_id <= last_id:
        if symmetric_string(str(product_id)):
            invalid_id_sum += product_id
        product_id += 1
    return invalid_id_sum


def sum_invalid_ids_ii(input_range):
    """return a sum of the invalid IDs found in the range"""
    fist_id = int(input_range.split("-")[0])
    last_id = int(input_range.split("-")[1])
    product_id = fist_id
    invalid_id_sum = 0
    while product_id <= last_id:
        if repeated_pattern(str(product_id)):
            invalid_id_sum += product_id
        product_id += 1
    return invalid_id_sum


def repeated_pattern(input_string):
    """check if the input_string is made of a repeating pattern"""
    string_length = len(input_string)
    for pattern_length in range(1, 1 + string_length // 2):
        pattern = input_string[:pattern_length]
        if string_length % pattern_length == 0:
            repeat_count = string_length // pattern_length
            pattern_count = input_string.count(pattern)
            if pattern_count == repeat_count:
                return True
    return False


def symmetric_string(input_string):
    """check if the input_string is a repeated pattern of characters"""
    if len(input_string) % 2 == 1:
        return False
    elif (
        input_string[: len(input_string) // 2] == input_string[len(input_string) // 2 :]
    ):
        return True
    else:
        return False


def extract_input_id_ranges(data):
    """Return a list of the input ranges"""
    return data.split(",")


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
