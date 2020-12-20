def run(env):

    if env == 1:
        fname = "day19.txt"
    elif env == 0:
        fname = "day19_test.txt"
    elif env == 2:
        fname = "day19_test2.txt"
    elif env == 3:
        fname = "day19_sergio.txt"
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

    max_len = max(messages, key=lambda x: len(x))
    print(f"==max_len== {max_len}")

    # print("8", set(cache["8"]))
    # print("42", set(cache["42"]))
    # print("11", set(cache["11"]))
    # print("31", set(cache["31"]))

    # i = 0
    # while i < 3:
    #     print("prefix: ", i)
    #     new_valids = set()
    #     for string in cache["42"]:
    #         for s in extended_valids:
    #             new_valids.add(string + s)
    #     extended_valids = new_valids
    #     i += 1
    #
    # i = 0
    # while i < 3:
    #     print("suffix: ", i)
    #     new_valids = set()
    #     for string in cache["31"]:
    #         for s in extended_valids:
    #             new_valids.add(s + string)
    #     extended_valids = new_valids
    #     i += 1

    # print(len(extended_valids & messages))

    more_valids = 0
    for ix, message in enumerate(sorted(messages)):
        # print("checking", ix, message)
        if message in valids:
            # print("is valid: ", original)
            more_valids += 1
            continue

        if not any(message.startswith(string) for string in cache["42"]):
            continue

        if not any(message.endswith(string) for string in cache["31"]):
            continue

        num42 = 0
        num31 = 0
        while any(message.startswith(string) for string in cache["42"]):
            for string in cache["42"]:
                if message.startswith(string):
                    message = message[len(string) :]
                    num42 += 1
        if not any(message.endswith(string) for string in cache["31"]):
            continue
        while any(message.startswith(string) for string in cache["31"]):
            for string in cache["31"]:
                if message.startswith(string):
                    message = message[len(string) :]
                    num31 += 1

        if (num42 >= 3 and num31 >= 1) and (num42 > num31) and not message:
            more_valids += 1
        else:
            print("42:", num42, "31:", num31)

    print(more_valids)

    # print(any("aaaabbaaaabbaaa".endswith(string) for string in cache["31"]))

    # 0: 8 | 11

    # l1 = 42 |


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
    # run(3)
    run(1)
    # run(2)
    # 282 no

    # 403 too high
