#!/usr/bin/env python
# coding: utf-8
#
# Day 14: Space Stoichiometry
#
# https://adventofcode.com/2019/day/14
#
# By Stefan Kruger

from collections import defaultdict
from math import ceil, floor


def read_data(filename="data/input14.data"):
    with open(filename) as f:
        return f.read().splitlines()


def parse_data(data):
    rules = {}
    for line in data:
        [left, right] = line.split(" => ")

        left_kv = {}
        for item in left.split(", "):
            [amount, name] = item.split(" ")
            left_kv[name] = int(amount)

        [factor, name] = right.split(" ")

        rules[name] = {"factor": int(factor), "parts": left_kv}

    return rules


def make_fuel(rules, q=1):
    parts = defaultdict(int)

    def react(chem, qty):
        ore = 0
        ratio = ceil(qty / rules[chem]["factor"])
        for (name, spec) in rules[chem]["parts"].items():
            new_qty = spec * ratio
            if name == "ORE":
                ore += new_qty
            else:
                if parts[name] < new_qty:
                    ore += react(name, new_qty - parts[name])
                parts[name] -= new_qty

        parts[chem] += ratio * rules[chem]["factor"]

        return ore

    return react("FUEL", q)


def find_max(rules):
    fuel = 1
    while True:
        ore = make_fuel(rules, fuel)
        if ore < 1000000000000:
            error = 1000000000000 / ore
            fuel = max(fuel + 1, floor(fuel * error))
        else:
            break

    return fuel - 1


if __name__ == "__main__":
    rules = parse_data(read_data())

    ore = make_fuel(rules)

    print(f"Part1: {ore}")
    print(f"Part2: {find_max(rules)}")
