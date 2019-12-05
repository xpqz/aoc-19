RESULT = 0

def read_data(filename="data/input05.data"):
    with open(filename) as f:
        return (list(map(int, f.read().split(","))))

def read_string(data):
    return (list(map(int, data.split(","))))


def add(data, ip, modes):
    params = data[ip+1:ip+4]
    data[params[2]] = (
        value(data, modes[0], params[0]) +
        value(data, modes[1], params[1]))
    return ip + 4


def mul(data, ip, modes):
    params = data[ip+1:ip+4]
    data[params[2]] = (
        value(data, modes[0], params[0]) *
        value(data, modes[1], params[1]))
    return ip + 4


def prn(data, ip, modes):
    param = data[ip+1]
    v = value(data, modes[0], param)
    if v != 0:
        print(v)
    return ip + 2


def jt(data, ip, modes):
    params = data[ip+1:ip+3]
    if value(data, modes[0], params[0]) != 0:
        return value(data, modes[1], params[1])
    return ip + 3


def jf(data, ip, modes):
    params = data[ip+1:ip+3]
    if value(data, modes[0], params[0]) == 0:
        return value(data, modes[1], params[1])
    return ip + 3


def lt(data, ip, modes):
    params = data[ip + 1:ip + 4]
    data[params[2]] = int(
        value(data, modes[0], params[0]) <
        value(data, modes[1], params[1]))
    return ip + 4


def eq(data, ip, modes):
    params = data[ip + 1:ip + 4]
    data[params[2]] = int(
        value(data, modes[0], params[0]) ==
        value(data, modes[1], params[1]))
    return ip + 4


OPCODES = {
    1: (add, 3),
    2: (mul, 3),
    3: (None, 1),
    4: (prn, 1),
    5: (jt, 2),
    6: (jf, 2),
    7: (lt, 3),
    8: (eq, 3),
    99: (None, 0)
}


def value(data, mode, param):
    if mode == 0:
        return data[param]
    return param


def parse_opcode(opcode):
    if opcode < 10:
        return [0] * OPCODES[opcode][1], opcode

    str_opc = str(opcode)
    op = int(str_opc[-2:])
    params = OPCODES[op][1]
    assert op in [1, 2, 3, 4, 5, 6, 7, 8, 99]

    return list(reversed(list(map(int, list(str_opc[:-2].zfill(params)))))), op


def run(code, input_data):
    data = code.copy()
    ip = 0
    while True:
        modes, opc = parse_opcode(data[ip])
        if opc == 3:
            data[data[ip+1]] = input_data
            ip += 2
            continue
        if opc == 99:
            break

        ip = OPCODES[opc][0](data, ip, modes)


if __name__ == "__main__":
    d = read_data()
    print("Part1: ", end="")
    run(d, 1)
    print("Part2: ", end="")
    run(d, 5)
