#!/usr/bin/env python
# coding: utf-8
#
# Advent of Code 2019
#
# Day 4: Secure Container
#
# https://adventofcode.com/2019/day/4
#
# By Stefan Kruger

import re

def is_valid(n, allow_multiples):
    ns = str(n)
    for i in range(len(ns)-1):
        if ns[i] > ns[i+1]:
            return False
        
    repeats = [x.group() for x in re.finditer(r"(.)\1+", ns)]
    if len(repeats) == 0:
        return False
    
    for r in repeats:
        if len(r) == 2:
            return True
        
    return allow_multiples


def count_valid(data, allow_multiples=True):
    count = 0
    for i in range(*data):
        if is_valid(i, allow_multiples):
            count += 1
            
    return count

if __name__ == "__main__":
    data = [236491, 713787]
    print(f"Part1: {count_valid(data)}")
    print(f"Part2: {count_valid(data, allow_multiples=False)}")




