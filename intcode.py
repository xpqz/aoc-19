from collections import defaultdict


def decode(program):
    return defaultdict(int, enumerate(map(int, program.split(','))))


def read_program(filename):
    with open(filename) as f:
        return [decode(f.read()), 0, 0, [], [], False]


def run(program, input_callback, poke=[]):
    ip = rb = 0
    mem = decode(program)
    for (addr, val) in poke:
        mem[addr] = val

    while True:
        op = mem[ip] % 100
        if op == 99:
            return
        size = [0, 4, 4, 2, 2, 3, 3, 4, 4, 2][op]
        args = [mem[ip+i] for i in range(1, size)]
        modes = [(mem[ip] // 10 ** i) % 10 for i in range(2, 5)]
        reads = [(mem[x], x, mem[x+rb])[m] for x, m in zip(args, modes)]
        writes = [(x, None, x+rb)[m] for x, m in zip(args, modes)]
        ip += size
        if op == 1:
            mem[writes[2]] = reads[0] + reads[1]
        elif op == 2:
            mem[writes[2]] = reads[0] * reads[1]
        elif op == 3:
            mem[writes[0]] = input_callback()
        elif op == 4:
            yield reads[0]
        elif op == 5 and reads[0]:
            ip = reads[1]
        elif op == 6 and not reads[0]:
            ip = reads[1]
        elif op == 7:
            mem[writes[2]] = int(reads[0] < reads[1])
        elif op == 8:
            mem[writes[2]] = int(reads[0] == reads[1])
        elif op == 9:
            rb += reads[0]
        elif op not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 99]:
            raise Exception(f"Unexpected opcode: {op}")


def resume(state):
    # state = [mem, ip, rb, input, output, terminated]

    while True:
        op = state[0][state[1]] % 100
        if op == 99:
            state[5] = True
            return state
        size = [0, 4, 4, 2, 2, 3, 3, 4, 4, 2][op]
        args = [state[0][state[1]+i] for i in range(1, size)]
        modes = [(state[0][state[1]] // 10 ** i) % 10 for i in range(2, 5)]
        reads = [(state[0][x], x, state[0][x+state[2]])[m] for x, m in zip(args, modes)]
        writes = [(x, None, x + state[2])[m] for x, m in zip(args, modes)]

        state[1] += size

        if op == 1:
            state[0][writes[2]] = reads[0] + reads[1]
        elif op == 2:
            state[0][writes[2]] = reads[0] * reads[1]
        elif op == 3:
            if not state[3]:
                state[1] -= size   # underrun, reverse one step
                return state
            state[0][writes[0]] = state[3].pop(0)
        elif op == 4:
            state[4].append(reads[0])
        elif op == 5 and reads[0]:
            state[1] = reads[1]
        elif op == 6 and not reads[0]:
            state[1] = reads[1]
        elif op == 7:
            state[0][writes[2]] = int(reads[0] < reads[1])
        elif op == 8:
            state[0][writes[2]] = int(reads[0] == reads[1])
        elif op == 9:
            state[2] += reads[0]
        elif op not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 99]:
            raise Exception(f"Unexpected opcode: {op}")
