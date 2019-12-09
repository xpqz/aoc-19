#!/usr/bin/env python
# coding: utf-8
#
# Day 8: Space Image Format
#
# https://adventofcode.com/2019/day/8
#
# By Stefan Kruger

from collections import Counter
BLACK = 0
WHITE = 1
TRANSP = 2


def read_data(filename="data/input08.data"):
    with open(filename) as f:
        return list(map(int, list(f.read().splitlines()[0])))


def make_image(xmax, ymax, digits):
    nd = (d for d in digits)
    layers = []
    while True:
        layer = [[0] * xmax for _ in range(ymax)]
        for y in range(ymax):
            for x in range(xmax):
                try:
                    layer[y][x] = next(nd)
                except StopIteration:
                    return layers
        layers.append(layer)


def checksum(layers):
    best = None
    for layer in layers:
        c = Counter()
        for row in layer:
            c.update(row)
        if best is None:
            best = c
        elif c[0] < best[0]:
            best = c
    return best[1] * best[2]


def value(layers, x, y):
    layer = 0
    while layers[layer][y][x] == TRANSP:
        layer += 1
    return layers[layer][y][x]


def decode(layers, xmax, ymax):
    image = [[0] * xmax for _ in range(ymax)]
    for y in range(ymax):
        for x in range(xmax):
            image[y][x] = value(layers, x, y)

    return image


def show(img):
    for row in img:
        s = "".join(list(map(str, row)))
        print(s.replace("0", " ").replace("1", "*"))


if __name__ == "__main__":
    data = read_data()
    layers = make_image(25, 6, data)

    print(f"Part1: {checksum(layers)}")
    show(decode(layers, 25, 6))
