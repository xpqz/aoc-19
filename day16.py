#!/usr/bin/env python
# coding: utf-8
#
# Day 16: Flawed Frequency Transmission
#
# https://adventofcode.com/2019/day/16
#
# By Stefan Kruger

from itertools import chain, cycle, repeat


def read_data(filename="data/input16.data"):
    with open(filename) as f:
        return list(map(int, list(f.read())))


def pattern(index):
    base_pattern = [0, 1, 0, -1]
    return chain.from_iterable(repeat(i, index) for i in base_pattern)


def part1(data):
    for _ in range(100):
        output_list = data[:]
        for i in range(len(data)):
            filter = cycle(pattern(i+1))
            next(filter)
            v = sum(d * next(filter) for d in data)
            output_list[i] = abs(v) % 10
        data = output_list

    return "".join(map(str, data[:8]))


def part2(data):
    """
    Repeat the input data 10_000 times and pick out a sub-sequence.

    Intractable to brute.

    Only the sub-sequence actually contributes, so can skip everything
    before. Each digit depends on the previous.
    """
    offset = int("".join(map(str, data[:7])))
    data = (data*10_000)[offset:]
    for _ in range(100):
        tot = 0
        for i in range(len(data)-1, -1, -1):
            data[i] = tot = (tot + data[i]) % 10

    return "".join(map(str, data[:8]))


if __name__ == "__main__":
    print(part1(read_data()))
    print(part2(read_data()))
