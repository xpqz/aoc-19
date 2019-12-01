# Advent of Code 2019
#
# Day 1: The Tyranny of the Rocket Equation
#
# Stefan Kruger


def read_data(filename="data/input01.data"):
    with open(filename) as f:
        return list(map(int, f.read().splitlines()))


def fuel(mass):
    return mass // 3 - 2


def total_fuel(mass):
    fuel_sum = 0
    while True:
        f = fuel(mass)
        if f <= 0:
            return fuel_sum
        mass = f
        fuel_sum += f


data = read_data()
print(f"Part1: {sum(map(fuel, data))}")
print(f"Part2: {sum(map(total_fuel, data))}")
