import random

def is_prime(number):
    if number > 1:
        small_prime_factors = [2, 3, 5, 7, 11, 13, 17]
        for i in small_prime_factors:
            if (number % i) == 0:
                return 0
        return 1
    else:
        return 0


def gcd(x, y):
    x = abs(x)
    y = abs(y)
    while x and y:
        if x > y:
            x -= y
        else:
            y -= x
    return x+y


def test_miller_rabin(p):
    d = p - 1
    s = 0
    while d % 2 == 0:
        d = d // 2
        s += 1
    d = int(d)
    p = int(p)

    for i in range(5):
        x = random.randint(2, p-1)
        gcd_number = gcd(x, p)
        if gcd_number > 1:
            return 0
        if (pow(x, d, p) == 1) or (pow(x, d, p) == (p-1)):
            return 1
        for r in range(1, s):
            xr = pow(x, d * (2**r), p)
            if xr == p-1:
                return 1
            if xr == 1:
                return 0
    return 0


def generate_prime_number():
    f = open('file.txt', 'a')
    while True:
        rand_numb = random.getrandbits(1024)
        if is_prime(rand_numb):
            if(test_miller_rabin(rand_numb)) == 1:
                break
            f.write(str(rand_numb)+"\n")
    return rand_numb


def euclid_algorithm(x, y):
    k = y
    q = [0, 0]
    p = [0, 1]
    x = abs(x)
    y = abs(y)
    while x != 1 and y != 1:
        if x > y:
            q.append(-(x // y))
            x %= y
        else:
            q.append(-(y // x))
            y %= x
    for i in range(2, len(q)):
        p.append((q[i]) * p[i - 1] + p[i - 2])
    return pow(p[-1], 1, k)


def GenerateKeyPair(p, q):
    n = p * q
    euler_n = (p-1)*(q-1)
    e = 2**16 + 1
    d = euclid_algorithm(e, euler_n)
    return d, p, q, n, e


def Encrypt(m, e, n):
    c = pow(m, e, n)
    return c


def Decrypt(c, d, n):
    m = pow(c, d, n)
    return m


def Sign(m, d, n):
    s = pow(m, d, n)
    return m, s


def Verify(m, s, e, n):
    if pow(s, e, n) == m:
        return 1
    else:
        return 0


def SendKey(e1, k, d, n, n1):
    s = pow(k, d, n)
    s1 = pow(s, e1, n1)
    k1 = pow(k, e1, n1)
    return k1, s1


def ReceiveKey(d1, n1, k1, s1):
    k = pow(k1, d1, n1)
    s = pow(s1, d1, n1)
    return k, s


if __name__ == '__main__':
    while True:
        p = generate_prime_number()
        q = generate_prime_number()
        p1 = generate_prime_number()
        q1 = generate_prime_number()
        if (p*q) <= (p1*q1):
            break

    print("A generated number p: ", p)
    print("A generated number q: ", q)
    print("B generated number p: ", p1)
    print("B generated number q: ", q1)
    print("------------------------------------------")

    A_keys = []
    A_keys = GenerateKeyPair(p, q)
    A_d = A_keys[0]
    A_n = A_keys[3]
    A_e = A_keys[4]
    print("A Secret key", A_d)
    print("A open keys", A_n, A_e)
    B_keys = []
    B_keys = GenerateKeyPair(p1, q1)
    B_n = B_keys[3]
    B_e = B_keys[4]
    B_d = B_keys[0]
    print("B Secret key", B_d)
    print("B open keys", B_n, B_e)

    M = random.randint(100, 999999)
    print("A want to send", M)
    C = Encrypt(M, B_e, B_n)
    print("A encrypt this message", C)
    M1 = Decrypt(C, B_d, B_n)
    print("B decrypt this message", M1)
    if M == M1:
        print("Messages is equals!")
    else:
        print("Messages is different!")
    print("A want to sign her message")
    A_signature = Sign(M, A_d, A_n)
    print("A signature is ", A_signature[1])
    print("B check signature")
    if Verify(A_signature[0], A_signature[1], A_e, A_n):
        print("Signature is valid")
    else:
        print("Signature is not valid")

    K = random.randint(100, 999999)
    Message = SendKey(B_e, K, A_d, A_n, B_n)
    print(Message)
    Message1 = ReceiveKey(B_d, B_n, Message[0], Message[1])
    print(Message1)
    if Verify(Message1[0], Message1[1], A_e, A_n):
        print("Signature is valid")
    else:
        print("Signature is not valid")

    # M2 = random.randint(100, 9999999)
    # Server_Public_modulus = 109392857305694839508355539668505497970851986289272735952976311087642307856122058616375539758600405189505230764873096869210030813911533839975852363201391584197825771148241259059222677913253822030295841899634529722017585673588354209373210118540718334768514367871226104940584080104277463806615536073409629399893
    # Server_Public_exponent = 65537
    # M2_Signature = Sign(M2, A_d, A_n)
    # C2 = Encrypt(M2, Server_Public_exponent, Server_Public_modulus)
    # C2_Signature = Encrypt(M2_Signature[1], Server_Public_exponent, Server_Public_modulus)
    #
    # print("Message = ", M2)
    # print("C2", C2)
    # print("C2_Signature", C2_Signature)
    # print("A_n:", A_n)
    # print("A_e:", A_e)

