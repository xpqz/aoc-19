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


CODE = read_data()


def read_string(data):
    return (list(map(int, data.split(","))))


def add(data, ip, modes):
    params = data[ip+1:ip+4]
    data[params[2]] = (
        value(data, modes[0], params[0]) +
        value(data, modes[1], params[1]))
    return ip + 4


def mul(data, ip, modes):
    params = data[ip+1:ip+4]
    data[params[2]] = (
        value(data, modes[0], params[0]) *
        value(data, modes[1], params[1]))
    return ip + 4


def jt(data, ip, modes):
    params = data[ip+1:ip+3]
    if value(data, modes[0], params[0]) != 0:
        return value(data, modes[1], params[1])
    return ip + 3


def jf(data, ip, modes):
    params = data[ip+1:ip+3]
    if value(data, modes[0], params[0]) == 0:
        return value(data, modes[1], params[1])
    return ip + 3


def lt(data, ip, modes):
    params = data[ip + 1:ip + 4]
    data[params[2]] = int(
        value(data, modes[0], params[0]) <
        value(data, modes[1], params[1]))
    return ip + 4


def eq(data, ip, modes):
    params = data[ip + 1:ip + 4]
    data[params[2]] = int(
        value(data, modes[0], params[0]) ==
        value(data, modes[1], params[1]))
    return ip + 4


OPCODES = {
    1: (add, 3),
    2: (mul, 3),
    3: (None, 1),
    4: (None, 1),
    5: (jt, 2),
    6: (jf, 2),
    7: (lt, 3),
    8: (eq, 3),
    99: (None, 0)
}


def value(data, mode, param):
    if mode == 0:
        return data[param]
    return param


def parse_opcode(opcode):
    if opcode < 10:
        return [0] * OPCODES[opcode][1], opcode
    str_opc = str(opcode)
    op = int(str_opc[-2:])
    params = OPCODES[op][1]
    return list(reversed(list(map(int, list(str_opc[:-2].zfill(params)))))), op


def run(phase_setting, input_data):
    data = CODE.copy()
    ip = 0
    phase_consumed = False
    while True:
        modes, opc = parse_opcode(data[ip])
        if opc == 3:
            if not phase_consumed:
                data[data[ip + 1]] = phase_setting
                phase_consumed = True
            else:
                data[data[ip + 1]] = input_data
            ip += 2
            continue
        elif opc == 4:
            param = data[ip+1]
            v = value(data, modes[0], param)
            return v
        if opc == 99:
            break

        ip = OPCODES[opc][0](data, ip, modes)


def maximise():
    best = None
    for phase_setting in list(permutations(list(range(5)))):
        input_data = 0

        for phase in phase_setting:
            result = run(phase, input_data)
            input_data = result

        if best is None or result > best:
            best = result
    return best


if __name__ == "__main__":
    print(f"Part1: {maximise()}")
