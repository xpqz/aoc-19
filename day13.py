#!/usr/bin/env python
# coding: utf-8
#
# Day 13: Care Package
#
# https://adventofcode.com/2019/day/13
#
# By Stefan Kruger

from intcode import run, resume, decode
from itertools import zip_longest


def read_data(filename="data/input13.data"):
    with open(filename) as f:
        return f.read()


def cmp(b, a):
    return (a > b) - (a < b)


def chunk(iterator, chunk_size):
    return zip_longest(*[iter(iterator)] * chunk_size)


def play(program):
    code = decode(program)
    code[0] = 2
    state = [code, 0, 0, [0], [], False]
    score = 0
    while state[5] is False:
        state = resume(state)
        ball = 0
        paddle = 0
        for item in chunk(state[4], 3):
            if item[0] == -1 and item[1] == 0:
                score = item[2]
            elif item[2] == 4:
                ball = item[0]
            elif item[2] == 3:
                paddle = item[0]

        # just track the x-position of the ball
        state[3].append(cmp(paddle, ball))
        state[4] = []  # reset output buffer

    return score


if __name__ == "__main__":
    program = read_data()

    out = run(program, lambda: 1)

    blocks = sum(1 for item in chunk(out, 3) if item[2] == 2)
    print(f"Part1: {blocks}")

    print(f"Part2: {play(program)}")
