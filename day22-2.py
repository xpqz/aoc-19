"""
Too hard for me. Solution after reading the following explanation:

https://www.reddit.com/r/adventofcode/comments/ee0rqi/2019_day_22_solutions/fbnkaju/

Note: number of cards is a prime number.

The set of card shuffles are linear combinations ax + b -- a is the increment between cards
and b the offset (first card), all mod the number of cards.

Part 2 is a geometric progression.

"""
import aoc


def inv(n, cards):
    # Modular inverse of n. As number of cards is prime, use Euler's theorem
    return pow(n, cards - 2, cards)


def parse_data(data, cards):
    offset = 0
    increment = 1

    for line in data:
        if line.startswith("deal into"):
            increment *= -1
            increment %= cards
            offset += increment
            offset %= cards
        elif line.startswith("cut"):
            offset += aoc.ints(line)[0] * increment
            offset %= cards
        elif line.startswith("deal with"):
            increment *= inv(aoc.ints(line)[0], cards)
            increment %= cards
        else:
            raise Exception("Unexpected command")

    return offset, increment


def nth(offset, increment, n, cards):
    return (offset + n * increment) % cards


def seq(offset, increment, iterations, cards):
    # calculate (incr, offs) for the number of iterations of the process
    # incr = increment^iterations
    incr = pow(increment, iterations, cards)

    # offs = 0 + offset * (1 + increment + increment^2 + ... + increment^iterations)
    # use geometric series.
    offs = offset * (1 - incr) * inv((1 - increment) % cards, cards)
    offs %= cards

    return offs, incr


if __name__ == "__main__":
    cards = 119315717514047
    iterations = 101741582076661

    offset, increment = parse_data(aoc.lines("data/input22.data"), cards)
    offset, increment = seq(offset, increment, iterations, cards)
    print(nth(offset, increment, 2020, cards))
