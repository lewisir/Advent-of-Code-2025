"""
--- Advent of Code 2025 ---
--- Day 6:  ---
https://adventofcode.com/2025/day/6
"""

from time import perf_counter

TEST = False

DAY = "6"
REAL_INPUT = "Advent-of-Code-2025/Day" + DAY + "/input_day" + DAY + ".txt"
TEST_INPUT = "Advent-of-Code-2025/Day" + DAY + "/input_test.txt"

if TEST:
    FILENAME = TEST_INPUT
else:
    FILENAME = REAL_INPUT


def main():
    """Main program"""
    data = get_input_data(FILENAME)
    vertical_data = process_data(data)
    print(f"Homework total Psrt I {calculate_homework(vertical_data)}")


def calculate_homework(vertical_data):
    """return the total value of each column added or multiplied together depending on the operand"""
    homework_total = 0
    for col in range(len(vertical_data[0])):
        if vertical_data[-1][col] == "+":
            operand = plus_op
            col_total = 0
        else:
            operand = multiply_op
            col_total = 1
        for row in range(len(vertical_data) - 1):
            col_total = operand(col_total, vertical_data[row][col])
        homework_total += col_total
    return homework_total


def plus_op(num1, num2):
    """return the sum of the numbers"""
    return num1 + num2


def multiply_op(num1, num2):
    """return the product of the numbers"""
    return num1 * num2


def process_data(data):
    """Process the data converting string to numbers and capturing the operations as text"""
    processed_data = []
    for line in data:
        if line.count("+") > 0 or line.count("*") > 0:
            processed_data.append(line.split())
        else:
            num_list = [int(x) for x in line.split()]
            processed_data.append(num_list)
    return processed_data


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
