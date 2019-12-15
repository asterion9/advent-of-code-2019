from functools import reduce

input = "124075-580769"


def parse_input_as_digits(input_string):
    return [[int(digit) for digit in number] for number in input_string.split("-")]


def parse_input_as_number(input_string):
    return [int(number) for number in input_string.split("-")]


def concat_digit(digits):
    return reduce(lambda x, y: x * 10 + y, digits)


def get_groups(digits):
    cur_group_num = 0
    cur_group_digit = ""
    for digit in digits:
        if digit == cur_group_digit:
            cur_group_num += 1
        else:
            yield cur_group_num
            cur_group_digit = digit
            cur_group_num = 1
    yield cur_group_num


def is_valid_pass_ex2(number):
    digits = str(number)
    for i in range(1, len(digits)):
        if digits[i-1] > digits[i]:
            return False
    groups = set(get_groups(digits[:]))
    return 2 in groups


def is_valid_pass_ex1(number):
    digits = str(number)
    adjacent = False
    for i in range(1, len(digits)):
        if digits[i-1] > digits[i]:
            return False
        if digits[i-1] == digits[i]:
            adjacent = True
    return adjacent


def brute_force_candidate(cur_num, max_num):
    for candidate in range(cur_num, max_num+1):
        if is_valid_pass_ex2(candidate):
            yield candidate
    return


if __name__ == '__main__':
    pass_range = parse_input_as_number(input)
    nb_candidate = sum(1 for candidate in brute_force_candidate(*pass_range))
    print(nb_candidate)
