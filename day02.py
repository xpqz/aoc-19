#!/usr/bin/env python
# coding: utf-8
#
# Advent of Code 2019
#
# Day 2: 1202 Program Alarm
#
# https://adventofcode.com/2019/day/2
#
# By Stefan Kruger

def read_data(filename="data/input02.data"):
    with open(filename) as f:
        return (list(map(int, f.read().split(","))))


class Done(Exception):
    pass


def run(code, noun, verb):
    data = code.copy()
    ip = 0
    data[1] = noun
    data[2] = verb
    while True:
        instr = data[ip:ip+4]
        opc = instr[0]
        if opc == 99:
            return data[0]
        i1, i2, out = instr[1:]
        if opc == 1:
            data[out] = data[i1] + data[i2]
        else:
            data[out] = data[i1] * data[i2]
        ip += 4


if __name__ == "__main__":
    d = read_data()
    print(f"Part1: {run(d, 12, 2)}")

    result = 0
    try:
        for n in range(100):
            for v in range(100):
                val = run(d, n, v)
                if val > 19690720:
                    continue
                if val == 19690720:
                    result = 100 * n + v
                    raise Done
    except Done:
        pass

    print(f"Part2: {result}")
