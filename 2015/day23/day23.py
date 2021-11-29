with open("input23.txt") as f:
    instructions = [line.strip() for line in f]

index = 0
# registers = {"a": 0, "b": 0}
registers = {"a": 1, "b": 0}
while True:
    if index >= len(instructions):
        break
    instruction = instructions[index]
    if instruction.startswith("hlf"):
        register = instruction[4]
        registers[register] = registers[register] // 2
        index += 1
        continue

    if instruction.startswith("tpl"):
        register = instruction[4]
        registers[register] = registers[register] * 3
        index += 1
        continue

    if instruction.startswith("inc"):
        register = instruction[4]
        registers[register] = registers[register] + 1
        index += 1
        continue
    if instruction.startswith("jmp"):
        offset = int(instruction[4:])
        index += offset
        continue

    if instruction.startswith("jie"):
        register = instruction[4]
        if registers[register] % 2 != 0:
            index += 1
            continue
        offset = int(instruction[7:])
        index += offset
        continue

    if instruction.startswith("jio"):
        register = instruction[4]
        if registers[register] != 1:
            index += 1
            continue
        offset = int(instruction[7:])
        index += offset
        continue
    print(instruction, "unknown")
    break

print(registers["b"])
