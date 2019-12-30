
import re
from blist import blist


def read_data(filename="data/input22.data"):
    with open(filename) as f:
        return f.read().splitlines()


def deal_with_increment2(stack, increment):
    return [stack[0]] + blist(reversed(
        [stack[(i*increment) % len(stack)] for i in range(1, len(stack))]
    ))


def deal_with_increment(stack, increment):
    new_stack = blist(stack)
    pos = 0
    for i in range(len(stack)):
        new_stack[pos] = stack[i]
        pos = (pos + increment) % len(stack)
    return new_stack


def deal_into_new_stack(stack):
    return blist(reversed(stack))


def cut(stack, amount):
    return stack[amount:] + stack[:amount]


def parse_data(data):
    commands = []
    for l in data:
        if l.startswith("deal with increment"):
            commands.append((deal_with_increment, int(re.findall(r'-?\d+', l)[0])))
        elif l.startswith("cut"):
            commands.append((cut, int(re.findall(r'-?\d+', l)[0])))
        elif l == "deal into new stack":
            commands.append((deal_into_new_stack, None))
        else:
            raise Exception("Unexpected command")

    return commands


def apply_commands(commands, stack):
    for (fn, arg) in commands:
        print(stack.index(2020))
        if arg is not None:
            stack = fn(stack, arg)
        else:
            stack = fn(stack)

    return stack


if __name__ == "__main__":
    # stack = apply_commands(parse_data(read_data()), blist(range(10_007)))
    # print(f"Part1: {stack.index(2_019)}")

    # stack = apply_commands(parse_data(read_data()), blist(range(10_007)))

    # length_p2 = 11_931_571_751_4047
    s = 10
    for i in range(1, s):
        print(deal_with_increment(blist(range(s)), i))
