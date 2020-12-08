with open("day8.txt") as f:
    data = [d.strip() for d in f]

operations = []


acc = 0
for elem in data:
    operation, num = elem.split(" ")
    num = int(num)
    operations.append((operation, num))

ix = 0
seen = set()
while True:
    if ix in seen:
        print(acc)
        break
    else:
        seen.add(ix)
    next_op = operations[ix]
    operation, num = next_op
    if operation == "acc":
        acc += num
        ix += 1
    elif operation == "jmp":
        ix += num
    elif operation == "nop":
        ix += 1

operations = list(operations)
jmps = [ix for ix, op in enumerate(operations) if op[0] == "jmp"]
nop = [ix for ix, op in enumerate(operations) if op[0] == "nop"]


def attempt(operations):
    acc = 0
    ix = 0
    seen = set()
    while True:
        if ix > len(operations) - 1:
            print(acc)
            raise ValueError
        if ix in seen:
            break
        else:
            seen.add(ix)
        next_op = operations[ix]
        operation, num = next_op
        if operation == "acc":
            acc += num
            ix += 1
        elif operation == "jmp":
            ix += num
        elif operation == "nop":
            ix += 1
    return False


ops = operations
while jmps or nop:
    jmps_replaced = False
    nop_replaced = False
    if jmps:
        jmps_replaced = True
        rep = jmps.pop()
        ops[rep] = ("nop", ops[rep][1])
    else:
        nop_replaced = True
        rep = nop.pop()
        ops = list(operations)
        ops[rep] = ("jmp", ops[rep][1])
    attempt(ops)
    if jmps_replaced:
        ops[rep] = ("jmp", ops[rep][1])
    else:
        ops[rep] = ("nop", ops[rep][1])
