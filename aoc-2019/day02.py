import intcode

input_intcode = [int(code) for code in
                 "1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,13,1,19,1,19,9,23,1,5,23,27,1,27,9,31,1,6,31,35,2,35,9,39,1,39,6,43,2,9,43,47,1,47,6,51,2,51,9,55,1,5,55,59,2,59,6,63,1,9,63,67,1,67,10,71,1,71,13,75,2,13,75,79,1,6,79,83,2,9,83,87,1,87,6,91,2,10,91,95,2,13,95,99,1,9,99,103,1,5,103,107,2,9,107,111,1,111,5,115,1,115,5,119,1,10,119,123,1,13,123,127,1,2,127,131,1,131,13,0,99,2,14,0,0"
                     .split(",")]
test1_intcode = [int(code) for code in "1,9,10,3,2,3,11,0,99,30,40,50".split(",")]
test2_intcode = [int(code) for code in "1,0,0,0,99".split(",")]
test3_intcode = [int(code) for code in "2,3,0,3,99".split(",")]
test4_intcode = [int(code) for code in "2,4,4,5,99,0".split(",")]
test5_intcode = [int(code) for code in "1,1,1,4,99,5,6,0,99".split(",")]


input_target_number = 19690720


def run_exo(code, noun=None, verb=None):
    code = code.copy()
    if noun is not None:
        code[1] = noun
    if verb is not None:
        code[2] = verb
    intcode.run_code(code)
    return code


def exo1():
    print(run_exo(input_intcode, 12, 2)[0])


def exo2():
    for verb in range(100):
        for noun in range(100):
            if run_exo(input_intcode, noun, verb)[0] == input_target_number:
                print(f'100 * {noun} + {verb} = {100 * noun + verb}')
                exit(1)


if __name__ == '__main__':
    exo2()
