#!/usr/bin/env python
# coding: utf-8
#
# Day 17: Set and Forget
#
# https://adventofcode.com/2019/day/17
#
# By Stefan Kruger

from intcode import poke, read_program, resume
import re


class Found(Exception):
    pass


def make_graph(code):
    state = resume(code)
    g = set()
    y = 1
    x = 1
    for i in state[4]:
        # ch = p(i)
        ch = str(chr(i))
        if ch in {"#", "^"}:
            g.add((x, y))
        if ch in "<>^v":
            pos = (x, y)
            heading = ch
        if ch == "\n":
            y += 1
            x = 1
        else:
            x += 1

    return g, pos, heading


def find_intersections(g, xmax, ymax):
    intersects = set()
    for y in range(1, ymax+1):
        for x in range(1, xmax + 1):
            if {(x, y), (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)} <= g:
                intersects.add((x, y))
    return intersects


def alignment(intersects):
    return sum((x[0]-1)*(x[1]-1) for x in intersects)


def make_path(g, xmax, ymax, pos, heading):
    """
    1. Follow in straight line for as long as possible.
    2. Go straight through any crossing.
    """
    def nh(heading, turn):
        if heading == ">":
            return {"R": "v", "L": "^"}[turn]
        if heading == "<":
            return {"R": "^", "L": "v"}[turn]
        if heading == "^":
            return {"R": ">", "L": "<"}[turn]
        if heading == "v":
            return {"R": "<", "L": ">"}[turn]
        else:
            raise Exception("Unexpected heading")

    def next_in_heading(pos, heading):
        return {
            "<": (pos[0] - 1, pos[1]), ">": (pos[0] + 1, pos[1]),
            "^": (pos[0], pos[1] - 1), "v": (pos[0], pos[1] + 1)
        }[heading]

    path = []
    steps = 0

    while True:
        while True:
            new_pos = next_in_heading(pos, heading)
            if new_pos not in g:
                break
            pos = new_pos
            steps += 1

        if steps > 0:
            path.append(steps)
            steps = 0

        for turn in {"L", "R"}:
            new_heading = nh(heading, turn)
            new_pos = next_in_heading(pos, new_heading)
            if new_pos in g:
                heading = new_heading
                path.append(turn)
                break
        else:  # nobreak
            break   # No more path to consume to either left or right

    return path


def encode(values):
    return list(map(ord, ",".join(map(str, values))+"\n"))


def partition(path):
    """
    Split the path into three repeating operations, each with fewer than 20 chars.

    Start from the beginning with gradually longer regexes, making the A sequence.
    Remove all matches, and try the same, now making B.
    Same for C -- if when we remove all C-matches we have an empty string, we've
    found a solution.

    Demand that each sequence starts with a turn -- this may or may not be true
    in the general case, but works for the given input set.
    """

    def rex(maxc):
        return r"^([LR][\w,]{4," + f"{maxc}" + r"},)"

    string_path = ",".join(map(str, path)) + ","
    valid = []
    try:
        for amax in range(4, 18):
            expr = re.compile(rex(amax))
            a = expr.findall(string_path)
            if not a:
                continue
            newpath = string_path.replace(a[0], "")
            if newpath[0] not in "LR":
                continue

            for bmax in range(4, 18):
                expr = re.compile(rex(bmax))
                b = expr.findall(newpath)
                if not b:
                    continue
                newbpath = newpath.replace(b[0], "")
                if newbpath[0] not in "LR":
                    continue

                for cmax in range(4, 18):
                    expr = re.compile(rex(cmax))
                    c = expr.findall(newbpath)
                    if not c:
                        continue
                    newcpath = newbpath.replace(c[0], "")
                    if newcpath == "":
                        valid = [a[0], b[0], c[0]]
                        raise Found
    except Found:
        pass

    if valid:
        s = string_path.replace(valid[0], "A") \
                       .replace(valid[1], "B") \
                       .replace(valid[2], "C")

        main = list(s)
        A = encode(valid[0][:-1].split(","))
        B = encode(valid[1][:-1].split(","))
        C = encode(valid[2][:-1].split(","))

        return encode(main) + A + B + C + [ord("n"), ord("\n")]

    raise Exception("No partition found")


if __name__ == "__main__":
    code = read_program("data/input17.data")
    g, bot, heading = make_graph(code)
    xmax = max(n[0] for n in g)
    ymax = max(n[1] for n in g)
    intersects = find_intersections(g, xmax, ymax)
    print(f"Part1: {alignment(intersects)}")

    # Part 2
    path = make_path(g, xmax, ymax, bot, heading)
    instr = partition(path)

    code = read_program("data/input17.data")
    poke(code, 0, 2)  # wake the robot
    code[3] = instr

    resume(code)

    print(f"Part2: {code[4][-1]}")
