import math

hexToBinary = """
0 = 0000
1 = 0001
2 = 0010
3 = 0011
4 = 0100
5 = 0101
6 = 0110
7 = 0111
8 = 1000
9 = 1001
A = 1010
B = 1011
C = 1100
D = 1101
E = 1110
F = 1111
""".strip().split(
    "\n"
)
hexToBinary = dict(k.split(" = ") for k in hexToBinary)


def decode_hex(line):
    parts = []
    for elem in line:
        parts.append(hexToBinary[elem])
    return "".join(parts)


def parse(s, count=None):
    if s.count("0") == len(s):
        return [], len(s)
    i = 0
    nums = []
    while i < len(s) and (count is None or len(nums) < count):
        if s[i:].count("0") == len(s[i:]):
            i += len(s[i])
            break
        version = int(s[i : i + 3], 2)
        i += 3
        typeId = int(s[i : i + 3], 2)
        i += 3
        b = s[i]
        if typeId == 4:
            ns = []
            while b != "0":
                i += 1
                packet = s[i : i + 4]
                i += 4
                ns.append(packet)
                b = s[i]
            i += 1
            packet = s[i : i + 4]
            i += 4
            ns.append(packet)
            nums.append(
                {
                    "version": version,
                    "int": int("".join(ns), 2),
                    "type": typeId,
                }
            )
            if i >= len(s):
                break
            if s[i:].count("0") == len(s[i:]):
                i += len(s[i:])
            continue
        lengthTypeId = b
        if lengthTypeId == "0":
            i += 1
            subPacketsTotalLength = int(s[i : i + 15], 2)
            i += 15
            res = [{"version": version, "type": typeId}]
            subResult, _ = parse(s[i : i + subPacketsTotalLength])
            res.append(subResult)
            nums.append(res)
            i += subPacketsTotalLength
        elif lengthTypeId == "1":
            i += 1
            subPacketCount = int(s[i : i + 11], 2)
            i += 11

            res = [{"version": version, "type": typeId}]
            subResult, delta = parse(s[i:], subPacketCount)
            res.append(subResult)
            nums.append(res)
            i += delta
    return nums, i


def flatten(x):
    return list(_flatten(x))


def _flatten(x):
    if isinstance(x, list):
        for elem in x:
            yield from _flatten(elem)
    else:
        yield x


def run(data, comp=False):
    print("run for", data)
    decoded = decode_hex(data)
    dec = parse(decoded)[0]
    res1 = flatten(parse(decoded)[0])
    totalVersion = 0
    for elem in res1:
        totalVersion += elem["version"]
    if comp:
        print("res", compute(dec[0]))
        print(dec[0])
    print("totalVersion", totalVersion)


def compute(l):
    if isinstance(l, dict):
        assert l["type"] == 4
        return l["int"]
    else:
        args = [compute(k) for k in l[1]]
        t = l[0]["type"]
        if t == 0:
            return sum(args)
        if t == 1:
            return math.prod(args)
        if t == 2:
            return min(args)
        if t == 3:
            return max(args)
        if t == 5:
            return 1 if args[0] > args[1] else 0
        if t == 6:
            return 1 if args[0] < args[1] else 0
        if t == 7:
            return int(args[1] == args[0])


run("D2FE28")
print("---------")
run("38006F45291200")
print("---------")
run("EE00D40C823060")
print("---------")
run("8A004A801A8002F478")
print("---------")
run("620080001611562C8802118E34")
print("---------")
run("C0015000016115A2E0802F182340")
print("---------")
run("A0016C880162017C3686B18A3D4780")
print("---------")


print("expect ", 3, end=" ")
run("C200B40A82", True)
print("expect ", 54, end=" ")
run("04005AC33890", True)
print("expect ", 7, end=" ")
run("880086C3E88112", True)
print("expect ", 9, end=" ")
run("CE00C43D881120", True)
print("expect ", 1, end=" ")
run("D8005AC2A8F0", True)
print("expect ", 0, end=" ")
run("F600BC2D8F", True)
print("expect ", 0, end=" ")
run("9C005AC2F8F0", True)
print("expect ", 1, end=" ")
run("9C0141080250320F1802104A08", True)
run(
    "E058F79802FA00A4C1C496E5C738D860094BDF5F3ED004277DD87BB36C8EA800BDC3891D4AFA212012B64FE21801AB80021712E3CC771006A3E47B8811E4C01900043A1D41686E200DC4B8DB06C001098411C22B30085B2D6B743A6277CF719B28C9EA11AEABB6D200C9E6C6F801F493C7FE13278FFC26467C869BC802839E489C19934D935C984B88460085002F931F7D978740668A8C0139279C00D40401E8D1082318002111CE0F460500BE462F3350CD20AF339A7BB4599DA7B755B9E6B6007D25E87F3D2977543F00016A2DCB029009193D6842A754015CCAF652D6609D2F1EE27B28200C0A4B1DFCC9AC0109F82C4FC17880485E00D4C0010F8D110E118803F0DA1845A932B82E200D41E94AD7977699FED38C0169DD53B986BEE7E00A49A2CE554A73D5A6ED2F64B4804419508B00584019877142180803715224C613009E795E58FA45EA7C04C012D004E7E3FE64C27E3FE64C24FA5D331CFB024E0064DEEB49D0CC401A2004363AC6C8344008641B8351B08010882917E3D1801D2C7CA0124AE32DD3DDE86CF52BBFAAC2420099AC01496269FD65FA583A5A9ECD781A20094CE10A73F5F4EB450200D326D270021A9F8A349F7F897E85A4020CF802F238AEAA8D22D1397BF27A97FD220898600C4926CBAFCD1180087738FD353ECB7FDE94A6FBCAA0C3794875708032D8A1A0084AE378B994AE378B9A8007CD370A6F36C17C9BFCAEF18A73B2028C0A004CBC7D695773FAF1006E52539D2CFD800D24B577E1398C259802D3D23AB00540010A8611260D0002130D23645D3004A6791F22D802931FA4E46B31FA4E4686004A8014805AE0801AC050C38010600580109EC03CC200DD40031F100B166005200898A00690061860072801CE007B001573B5493004248EA553E462EC401A64EE2F6C7E23740094C952AFF031401A95A7192475CACF5E3F988E29627600E724DBA14CBE710C2C4E72302C91D12B0063F2BBFFC6A586A763B89C4DC9A0",
    True,
)  # 1510980616914 too high 1510977819698
