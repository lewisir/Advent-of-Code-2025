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
    print(f"Homework total Part I {calculate_homework(vertical_data)}")
    new_number_columns = extract_number_column(data, find_common_space_positions(data))
    column_aligned_numbers = derive_column_aligned_numbers(new_number_columns)
    operators = extract_operators(data)
    print(
        f"Homework total Part II {new_calc_homework(column_aligned_numbers,operators)}"
    )


def new_calc_homework(numbers, operators):
    """return the homework calculation summing or multiplying each row of numbers"""
    homework_total = 0
    for x in range(len(operators)):
        if operators[x] == "+":
            operand = plus_op
            row_total = 0
        else:
            operand = multiply_op
            row_total = 1
        for number in numbers[x]:
            row_total = operand(row_total, number)
        homework_total += row_total
    return homework_total


def extract_operators(data):
    """return a list of the operators used for each column of numbers"""
    return data[-1].split()


def derive_column_aligned_numbers(number_string_data):
    """Return a list of the numbers(converted to integers) having produced the number passed on column alignment"""
    column_aligned_numbers = []
    for row in number_string_data:
        new_number_row = []
        for char_position in range(len(row[0])):
            new_number_list = []
            for number_position in range(len(row) - 1):
                new_number_list.append(row[number_position][char_position])
            new_number = int("".join(new_number_list))
            new_number_row.append(new_number)
        column_aligned_numbers.append(new_number_row)
    return column_aligned_numbers


def extract_number_column(data, space_positions):
    """Return a list of the number strings and the operator"""
    space_positions.append(len(data[0]))
    last_separator = 0
    number_string_columns = []
    for separator in space_positions:
        number_list = []
        for row in data:
            number_list.append(row[last_separator:separator])
        last_separator = separator + 1
        number_string_columns.append(number_list)
    return number_string_columns


def find_common_space_positions(data):
    """return a list of the positions of the spaces that are common across all lines"""
    common_space_positions_list = []
    for line in data:
        line_space_positions = set()
        for index, char in enumerate(line):
            if char == " ":
                line_space_positions.add(index)
        common_space_positions_list.append(line_space_positions)
    common_space_positions_set = common_space_positions_list[0]
    for index in range(1, len(common_space_positions_list)):
        common_space_positions_set.intersection_update(
            common_space_positions_list[index]
        )
    common_space_positions = list(common_space_positions_set)
    common_space_positions.sort()
    return common_space_positions


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
