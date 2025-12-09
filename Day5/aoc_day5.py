"""
--- Advent of Code 2025 ---
--- Day 5:  ---
https://adventofcode.com/2025/day/5
"""

from time import perf_counter

TEST = False

DAY = "5"
REAL_INPUT = "Advent-of-Code-2025/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2025/Day" + DAY + "/input_test.txt"

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT


def main():
    """Main program"""
    data = get_input_data(FILENAME)
    fresh_ranges, ingredient_ids = process_data(data)
    print(f"Fresh Ingredients Part I = {check_freshness(fresh_ranges, ingredient_ids)}")
    fresh_ranges.sort()
    consolidated_ranges = consolidate_ranges(fresh_ranges)
    all_fresh_ingredients = count_fresh_ingredients(consolidated_ranges)
    print(f"Total Fresh Ingredients Part II {all_fresh_ingredients}")


def count_fresh_ingredients(consolidated_ingredient_ranges):
    """Count the total number of fresh ingredients from the ranges"""
    ingredient_count = 0
    for ingredient_range in consolidated_ingredient_ranges:
        ingredient_count += ingredient_range[1] - ingredient_range[0] + 1
    return ingredient_count


def consolidate_ranges(fresh_ranges):
    """Work through the ranges and consolidation/combine them where they overlap and return a non-overlapping list of ranges"""
    consolidated_ranges = [fresh_ranges[0]]
    for index in range(1, len(fresh_ranges)):
        range_1 = consolidated_ranges[-1]
        range_2 = fresh_ranges[index]
        combined_ranges = combine_ranges(range_1, range_2)
        if len(combined_ranges) == 1:
            consolidated_ranges[-1] = combined_ranges[0]
        else:
            consolidated_ranges.append(combined_ranges[1])
    return consolidated_ranges


def combine_ranges(range_1, range_2):
    """return either a single range if the two ranges overlap, or the two separate ranges if they don't overlap. This relies on range_1_start being lower than range_2 start"""
    range_1_start, range_1_end = range_1
    range_2_start, range_2_end = range_2
    if range_2_start <= range_1_end:
        start = range_1_start
        end = max(range_1_end, range_2_end)
        return [(start, end)]
    else:
        return [range_1, range_2]


def check_freshness(fresh_ranges, ingredient_ids):
    """Check whether each ingredient is fresh and return the number that are"""
    fresh_ingredient_count = 0
    for ingredient in ingredient_ids:
        for fresh_range in fresh_ranges:
            start = fresh_range[0]
            end = fresh_range[1]
            if ingredient >= start and ingredient <= end:
                fresh_ingredient_count += 1
                break
    return fresh_ingredient_count


def process_data(data):
    fresh_ranges = []
    ingrediant_ids = []
    for line in data:
        if line.find("-") > 0:
            start_id = int(line[: line.find("-")])
            end_id = int(line[line.find("-") + 1 :])
            fresh_ranges.append((start_id, end_id))
        elif line == "":
            pass
        else:
            ingrediant_ids.append(int(line))
    return fresh_ranges, ingrediant_ids


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
