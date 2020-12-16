import math
import re
from functools import reduce


def process_rules(raw):
    rules = {}
    lines = raw.split("\n")
    for line in lines:
        key, r = line.split(": ")
        r1, r2 = r.split(" or ")
        i1, i2 = [int(k) for k in r1.split("-")]
        j1, j2 = [int(k) for k in r2.split("-")]
        rules[key] = set(range(i1, i2 + 1)) | set(range(j1, j2 + 1))
    return rules


def process_tickets(raw):
    nums = [set(int(i) for i in re.findall("\d+", r)) for r in raw.split("\n")[1:]]
    return nums


def process_tickets_list(raw):
    nums = [[int(i) for i in re.findall("\d+", r)] for r in raw.split("\n")[1:]]
    return nums


def process_ticket(raw):
    return [[int(i) for i in re.findall("\d+", r)] for r in raw.split("\n")[1:]][0]


def run(prod):
    file_name = "day16.txt" if prod else "day16_test.txt"
    with open(file_name) as f:
        data = f.read()

    raw_rules, raw_ticket, raw_tickets = data.split("\n\n")
    tickets = process_tickets(raw_tickets)
    # print(tickets)
    my_ticket = process_ticket(raw_ticket)

    rules = process_rules(raw_rules)
    all_valid = reduce(lambda x, y: x | y, rules.values())
    # print(all_valid)
    invalid_sum = 0
    valids = []
    for ticket in tickets:
        valid = True
        for invalid in ticket - all_valid:
            invalid_sum += invalid
            valid = False
        if valid:
            valids.append(ticket)
    print(invalid_sum)
    # print("valids: ", valids)

    valid_tickets = [t for t in process_tickets_list(raw_tickets) if set(t) in valids]

    res = solve(valid_tickets + [my_ticket], rules)
    print(res)
    prod = 1
    for key, value in res.items():
        if key.startswith("departure"):
            print(key, " ", value)
            prod *= my_ticket[value]
    print(prod)


def solve(tickets, rules):
    def solutions_fors(positions):
        sols = {}
        for position in range(len(tickets[0])):
            sols[position] = set()
            for solution in solutions_for(position):
                sols[position].add(solution)
        return sols

    def solutions_for(position):
        sol = []
        for rule, rule_nums in rules.items():
            if all(ticket[position] in rule_nums for ticket in tickets):
                sol.append(rule)
        return sol

    possible_solutions = solutions_fors(list(range(len(tickets[0]))))
    while any(len(x) > 1 for k, x in possible_solutions.items()):
        ordered_possibles = sorted(possible_solutions.items(), key=lambda x: len(x[1]))
        possible_solutions = dict()
        to_remove = set()
        for pos, sols in ordered_possibles:
            if len(sols) == 1:
                possible_solutions[pos] = sols
                to_remove.add(list(sols)[0])
            else:
                possible_solutions[pos] = sols - to_remove

    return {list(sols)[0]: pos for pos, sols in possible_solutions.items()}


if __name__ == "__main__":
    import time

    t0 = time.time()
    run(1)
    print("time: ", time.time() - t0)
    # run(0)
    # too low 141120
