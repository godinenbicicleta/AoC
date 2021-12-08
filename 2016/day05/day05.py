from hashlib import md5

i = "ojvtpuvg"
# i = "abc"


password = []
ix = 0
while len(password) < 8:
    h = md5(f"{i}{ix}".encode()).hexdigest()

    if h.startswith("00000"):
        password.append(h[5])
        print(ix, "\t", h, "\t", password)
    ix += 1

print("".join(password))

i = "ojvtpuvg"
# i = "abc"


password = [None] * 8
ix = 0
while not all(password):
    h = md5(f"{i}{ix}".encode()).hexdigest()

    if h.startswith("00000"):
        try:
            pos = int(h[5])
            val = h[6]
            if pos >= 0 and pos < len(password) and password[pos] is None:
                password[pos] = val

            print(ix, "\t", h, "\t", password)
        except ValueError as e:
            pass
    ix += 1

print("".join(password))
