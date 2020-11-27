import heapq
import re
from collections import Counter, deque

test_rules = [
    ("e", "H"),
    ("e", "O"),
    ("H", "HO"),
    ("H", "OH"),
    ("O", "HH"),
]


starting = "e"


def run(rules, molecule):

    words = []
    heapq.heappush(words, (-1, 0, "e"))
    seen = set()
    sr = {r[0][0] for r in rules}
    lm = len(molecule)

    molec_counter = Counter(molecule)

    def priority(word):
        return (
            abs(len(word) - len(molecule)),
            sum((molec_counter - Counter(word)).values()),
        )

    while words:

        _, steps, word = heapq.heappop(words)
        if word == molecule:
            return steps
        if word in seen:
            continue
        else:
            seen.add(word)

        lw = len(word)
        if lw >= lm:
            continue

        for i in range(lw):
            if word[i] not in sr:
                continue
            wordi = word[i:]
            wd = word[:i]

            for expr, sub in rules:
                if wordi.startswith(expr):
                    new = wordi.replace(expr, sub, 1)
                    new_word = wd + new
                    if new_word == molecule:
                        return steps + 1
                    if len(new_word) > lm:
                        continue
                    if new_word not in seen:
                        heapq.heappush(
                            words, (priority(new_word), steps + 1, new_word,),
                        )


#                        seen.add(new_word)


prod_rules = [
    ("Al", "ThF"),
    ("Al", "ThRnFAr"),
    ("B", "BCa"),
    ("B", "TiB"),
    ("B", "TiRnFAr"),
    ("Ca", "CaCa"),
    ("Ca", "PB"),
    ("Ca", "PRnFAr"),
    ("Ca", "SiRnFYFAr"),
    ("Ca", "SiRnMgAr"),
    ("Ca", "SiTh"),
    ("F", "CaF"),
    ("F", "PMg"),
    ("F", "SiAl"),
    ("H", "CRnAlAr"),
    ("H", "CRnFYFYFAr"),
    ("H", "CRnFYMgAr"),
    ("H", "CRnMgYFAr"),
    ("H", "HCa"),
    ("H", "NRnFYFAr"),
    ("H", "NRnMgAr"),
    ("H", "NTh"),
    ("H", "OB"),
    ("H", "ORnFAr"),
    ("Mg", "BF"),
    ("Mg", "TiMg"),
    ("N", "CRnFAr"),
    ("N", "HSi"),
    ("O", "CRnFYFAr"),
    ("O", "CRnMgAr"),
    ("O", "HP"),
    ("O", "NRnFAr"),
    ("O", "OTi"),
    ("P", "CaP"),
    ("P", "PTi"),
    ("P", "SiRnFAr"),
    ("Si", "CaSi"),
    ("Th", "ThCa"),
    ("Ti", "BP"),
    ("Ti", "TiTi"),
    ("e", "HF"),
    ("e", "NAl"),
    ("e", "OMg"),
]

prod_molecule = "CRnSiRnCaPTiMgYCaPTiRnFArSiThFArCaSiThSiThPBCaCaSiRnSiRnTiTiMgArPBCaPMgYPTiRnFArFArCaSiRnBPMgArPRnCaPTiRnFArCaSiThCaCaFArPBCaCaPTiTiRnFArCaSiRnSiAlYSiThRnFArArCaSiRnBFArCaCaSiRnSiThCaCaCaFYCaPTiBCaSiThCaSiThPMgArSiRnCaPBFYCaCaFArCaCaCaCaSiThCaSiRnPRnFArPBSiThPRnFArSiRnMgArCaFYFArCaSiRnSiAlArTiTiTiTiTiTiTiRnPMgArPTiTiTiBSiRnSiAlArTiTiRnPMgArCaFYBPBPTiRnSiRnMgArSiThCaFArCaSiThFArPRnFArCaSiRnTiBSiThSiRnSiAlYCaFArPRnFArSiThCaFArCaCaSiThCaCaCaSiRnPRnCaFArFYPMgArCaPBCaPBSiRnFYPBCaFArCaSiAl"


def run_reverse(rules, molecule):
    rules = [(v, k) for k, v in rules]
    words = deque([(0, molecule)])
    seen = set()
    sr = {r[0][0] for r in rules}
    goal = "e"
    it = 0

    while words:
        it += 1

        steps, word = words.pop()
        if it % 10000 == 0:
            print((steps, len(word)))
        if word == goal:
            return steps
        if word in seen:
            continue
        else:
            seen.add(word)

        if goal in word:
            continue
        lw = len(word)
        for i in range(lw):
            if word[i] not in sr:
                continue
            wordi = word[i:]
            wd = word[:i]

            for expr, sub in rules:
                if wordi.startswith(expr):
                    new = wordi.replace(expr, sub, 1)
                    new_word = wd + new
                    if new_word == goal:
                        return steps + 1
                    if goal in new_word:
                        continue
                    if new_word not in seen:
                        words.append((steps + 1, new_word))


if __name__ == "__main__":
    import time

    t = time.time()
    print(run(test_rules, "HOHOHO"))
    print(time.time() - t)
    t = time.time()
    print(run_reverse(test_rules, "HOHOHO"))
    print(time.time() - t)
    t = time.time()
    print(run_reverse(prod_rules, prod_molecule))
    print(time.time() - t)
