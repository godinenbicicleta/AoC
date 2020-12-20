def run(env):

    if env == 1:
        fname = "day19.txt"
    elif env == 0:
        fname = "day19_test.txt"
    else:
        raise FileNotFoundError
    with open(fname) as f:
        data = f.read()

    rules, messages = data.split("\n\n")
    rules = rules.split("\n")

    print(rules)
    print("=" * 10)

    # print(messages)

    rule_dict = {line.split(": ")[0]: line.split(": ")[1] for line in rules}
    print(rule_dict)
    # print("5", parse("5", rule_dict))
    # print("4", parse("4", rule_dict))
    # print("3", parse("3", rule_dict))
    # print("2", parse("2", rule_dict))
    # print("1", parse("1", rule_dict))
    # print("0", parse("0", rule_dict))

    # print("34", parse("34", rule_dict))
    # print("37", parse("37", rule_dict))

    # print(len(messages.split("\n")))
    valids = set(parse("0", rule_dict))
    # for i, v in enumerate(sorted(valids, key=lambda x: len(x))):
    #     if i < 10:
    #         print(v)
    #         continue
    #     break
    # for key, value in cache.items():
    #     if len(value) < 5:
    #         print("key: ", key, "value: ", value, "dict: ", rule_dict[key])

    messages = set(messages.split("\n"))
    print(len(valids & messages))


cache = {}


def parse(key, rule_dict):
    if key in cache:
        return cache[key]
    rd = rule_dict[key]
    # print("key: ", key, "rd: ", rd)
    if rd in ('"a"', '"b"'):
        res = [rd.strip('"')]
        cache[key] = res
        return res

    parsed = []
    for rule in rd.split("|"):
        r = []
        for elem in rule.split():
            if r:
                new_r = []
                for prev in r:
                    if isinstance(prev, str):

                        pd = parse(elem, rule_dict)
                        # print(f"prev: {prev}, elem: {elem} pd: {pd}, new_r: {new_r}")

                        if isinstance(pd, list):
                            for p in pd:
                                new_r.append(prev + p)
                        else:
                            new_r.append(prev + pd)
                    else:
                        pd = parse(elem, rule_dict)
                        # print(f"prev: {prev}, elem: {elem} pd: {pd}, new_r: {new_r} here")
                        new_r.append(prev + pd)
                r = new_r
            else:
                r = parse(elem, rule_dict)

        if parsed:
            new_parsed = []
            for prev in parsed:
                new_parsed.append(prev + r)
            parsed = new_parsed
        else:
            parsed.append(r)
    f = flatten(parsed)
    cache[key] = f
    # print(f"res for {key}: {f}")
    return f


def flatten(rule):
    def fl(r):
        for elem in r:
            if isinstance(elem, list):
                yield from fl(elem)
            else:
                yield elem

    return list(fl(rule))


def join(list_of_lists):
    if isinstance(list_of_lists[0], list) and len(list_of_lists) == 1:
        return join(list_of_lists[0])
    return list_of_lists


if __name__ == "__main__":
    # aaaabb, aaabab, abbabb, abbbab, aabaab, aabbbb, abaaab, or ababbb.
    # run(0)
    run(1)
