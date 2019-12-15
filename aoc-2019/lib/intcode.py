import itertools
import logging


class Operation:
    def __init__(self, operation, desc):
        self.execute = operation
        self.desc = desc
        self.type = type

    def __str__(self):
        return self.desc


class IntcodeVm:
    def __init__(self, intcode, input_c=itertools.repeat(None), output_c=lambda x: None):
        self.input_channel = input_c
        self.output_channel = output_c
        self.run_state = 0
        self.memory = intcode
        self.pointer = 0
        self.logger = logging.getLogger("IntcodeVm")
        self.operations = {
            1: Operation(lambda modes: self.write(modes[2], self.read(modes[0]) + self.read(modes[1])), "add"),
            2: Operation(lambda modes: self.write(modes[2], self.read(modes[0]) * self.read(modes[1])), "mul"),
            3: Operation(lambda modes: self.write(modes[0], self.read_in()), "in"),
            4: Operation(lambda modes: self.write_out(self.read(modes[0])), "out"),
            5: Operation(lambda modes: self.move_abs(self.read(modes[1])) if self.read(modes[0]) != 0 else self.move_rel(1), "ift"),
            6: Operation(lambda modes: self.move_abs(self.read(modes[1])) if self.read(modes[0]) == 0 else self.move_rel(1), "iff"),
            7: Operation(lambda modes: self.write(modes[2], 1 if self.read(modes[0]) < self.read(modes[1]) else 0), "less"),
            8: Operation(lambda modes: self.write(modes[2], 1 if self.read(modes[0]) == self.read(modes[1]) else 0), "equals"),
            99: Operation(lambda modes: self.write_err(1), "exit")
        }

    def stop(self, status):
        self.run_state = status

    def read_in(self):
        inputc_value = next(self.input_channel)
        self.logger.debug(f"read input {inputc_value}")
        return inputc_value

    def write_out(self, value):
        self.logger.debug(f"write output {value}")
        self.output_channel(value)

    def write_err(self, value):
        self.logger.debug(f"state {value}")
        self.run_state = value

    def read(self, mode):
        if mode:
            self.logger.debug(f"{self.pointer}: read {self.memory[self.pointer]}")
            read_val = self.memory[self.pointer]
        else:
            self.logger.debug(f"{self.pointer}: read [{self.memory[self.pointer]}]={self.memory[self.memory[self.pointer]]}")
            read_val = self.memory[self.memory[self.pointer]]
        self.pointer += 1
        return read_val

    def write(self, mode, value):
        if mode:
            self.logger.debug(f"{self.pointer}: write [{self.pointer}]={value}")
            self.memory[self.pointer] = value
        else:
            self.logger.debug(f"{self.pointer}: write [{self.memory[self.pointer]}]={value}")
            self.memory[self.memory[self.pointer]] = value
        self.pointer += 1

    def move_rel(self, value):
        self.logger.debug(f"move +{value}")
        self.pointer += value

    def move_abs(self, value):
        self.logger.debug(f"move to {value}")
        self.pointer = value

    def exec_tic(self):
        if self.run_state != 0:
            raise Exception(f"try running in non zero state")
        op_num = self.memory[self.pointer]
        operation = self.operations[op_num % 100]
        explicit_modes = [int(d) for d in reversed(str(op_num // 100))]
        modes = explicit_modes + [0, 0, 0]
        self.logger.debug(f"{self.pointer}: {self.memory[self.pointer:self.pointer+4]}")
        self.pointer += 1
        operation.execute(modes)
        return self.run_state

    def run_code(self):
        while self.exec_tic() == 0:
            pass
