#!/usr/bin/env python
# coding: utf-8
#
# Day 7: Amplification Circuit
#
# https://adventofcode.com/2019/day/7
#
# By Stefan Kruger


from itertools import permutations


def read_data(filename="data/input07.data"):
    with open(filename) as f:
        return (list(map(int, f.read().split(","))))


class Amplifier:
    def __init__(self, code):
        self.input = []
        self.output = []
        self.terminated = False
        self.data = code
        self.ip = 0
        self.opcodes = {
            1: (self.add, 3),
            2: (self.mul, 3),
            3: (None, 1),
            4: (None, 1),
            5: (self.jt, 2),
            6: (self.jf, 2),
            7: (self.lt, 3),
            8: (self.eq, 3),
            99: (None, 0)
        }

    def parse_opcode(self, opcode):
        if opcode < 10:
            return [0] * self.opcodes[opcode][1], opcode
        str_opc = str(opcode)
        op = int(str_opc[-2:])
        params = self.opcodes[op][1]
        return list(reversed(list(map(int, list(str_opc[:-2].zfill(params)))))), op

    def value(self, mode, param):
        if mode == 0:
            return self.data[param]
        return param

    def add(self, modes):
        params = self.data[self.ip+1:self.ip+4]
        self.data[params[2]] = (
            self.value(modes[0], params[0]) +
            self.value(modes[1], params[1]))
        self.ip += 4

    def mul(self, modes):
        params = self.data[self.ip+1:self.ip+4]
        self.data[params[2]] = (
            self.value(modes[0], params[0]) *
            self.value(modes[1], params[1]))
        self.ip += 4

    def jt(self, modes):
        params = self.data[self.ip+1:self.ip+3]
        if self.value(modes[0], params[0]) != 0:
            self.ip = self.value(modes[1], params[1])
        else:
            self.ip += 3

    def jf(self, modes):
        params = self.data[self.ip+1:self.ip+3]
        if self.value(modes[0], params[0]) == 0:
            self.ip = self.value(modes[1], params[1])
        else:
            self.ip += 3

    def lt(self, modes):
        params = self.data[self.ip + 1:self.ip + 4]
        self.data[params[2]] = int(
            self.value(modes[0], params[0]) <
            self.value(modes[1], params[1]))
        self.ip += 4

    def eq(self, modes):
        params = self.data[self.ip + 1:self.ip + 4]
        self.data[params[2]] = int(
            self.value(modes[0], params[0]) ==
            self.value(modes[1], params[1]))
        self.ip += 4

    def add_input(self, d):
        self.input.append(d)
        self.run()

    def run(self):
        while True:
            modes, opc = self.parse_opcode(self.data[self.ip])
            if opc == 3:
                if len(self.input) == 0:
                    return
                self.data[self.data[self.ip + 1]] = self.input.pop(0)
                self.ip += 2
            elif opc == 4:
                param = self.data[self.ip+1]
                v = self.value(modes[0], param)
                self.output.append(v)
                self.ip += 2
            elif opc == 99:
                self.terminated = True
                break
            else:
                self.opcodes[opc][0](modes)


def run_amplifiers(data, phases):
    amps = [Amplifier(data.copy()) for _ in range(5)]

    for phase, amp in zip(phases, amps):
        amp.add_input(phase)

    amps[0].add_input(0)

    while not amps[4].terminated:
        for i, amp in enumerate(amps):
            amps[(i+1) % 5].add_input(amp.output[-1])

    return amps[4].output[-1]


if __name__ == "__main__":
    d = read_data()
    part1 = max(
        run_amplifiers(d, phases)
        for phases in permutations(range(5))
    )

    print(f"Part1: {part1}")
    part2 = max(
        run_amplifiers(d, phases)
        for phases in permutations(range(5, 10)))
    )
    print(f"Part2: {part2}")
