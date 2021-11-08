import math


def read_text_from_file(your_filename):
    with open(your_filename, "r", encoding='UTF-8') as f:
        text_from_file = f.read()
    text_from_file = text_from_file.replace("\n", "")
    return text_from_file


def gcd(x, y):
    x = abs(x)
    y = abs(y)
    while x and y:
        if x > y:
            x -= y
        else:
            y -= x
    return x+y


def euclid_algorithm(x, y):
    if gcd(x, y) != 1:
        return 0
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


def solve_congruence(a, b, n):
    d = gcd(a, n)
    if d == 1:
        x = pow(b * euclid_algorithm(a, n), 1, n)
        return x
    elif d > 1:
        if b % d == 0:
            x0 = pow((b//d) * euclid_algorithm((a//d), (n//d)), 1, (n//d))
            x = []
            for i in range(d):
                x.append(x0 + i*(n//d))
            return x
        else:
            return 0


def find_popular_bigramms(filtered_text, flag):
    bigram_of_text = [filtered_text[i:i + 2] for i in range(0, len(filtered_text), 2)]
    if flag:
        return bigram_of_text
    frequency_of_bigrams = {}
    for bg in bigram_of_text:
        if bg not in frequency_of_bigrams:
            frequency_of_bigrams[bg] = round(bigram_of_text.count(bg) / len(bigram_of_text), 5)
    my_popular_bigrams = sorted(frequency_of_bigrams, key=frequency_of_bigrams.get, reverse=True)[:5]
    #print(my_popular_bigrams)
    return my_popular_bigrams


def convert_bigrams(list_bigramm, flag):
    possible_list_bigramm = []
    global russ_letters
    number_list = []
    for i in list_bigramm:
        number_list.append(russ_letters.find(i[0]) * len(russ_letters) + russ_letters.find(i[1]))
    if flag:
        return number_list
    for i in range(len(number_list)):
        for j in number_list[i + 1:]:
            possible_list_bigramm.append((number_list[i], j))
    print(possible_list_bigramm)
    return possible_list_bigramm


def find_key(filename):
    popular_bigrams = ["ст", "но", "то", "на", "ен"]
    global russ_letters
    clear_bigrams = convert_bigrams(popular_bigrams, 0)
    encrypted_bigrams = convert_bigrams(find_popular_bigramms(read_text_from_file(filename), 0), 0)
    #print(clear_bigrams)
    #print(encrypted_bigrams)
    keys = []
    for i in clear_bigrams:
        for j in encrypted_bigrams:
            a = solve_congruence((i[0]-i[1]), (j[0]-j[1]), (len(russ_letters))**2)
            if type(a) is list:
                for d in a:
                    b = pow((j[0] - (d * i[0])), 1, (len(russ_letters)) ** 2)
                    keys.append((d, b))
            elif a != 0:
                b = pow((j[0] - (a * i[0])), 1, (len(russ_letters))**2)
                keys.append((a, b))
    #print("Keys:", keys)
    return keys


def entropy_func(filtered_text):
    frequency = []
    global russ_letters
    for i in russ_letters:
        frequency.append((filtered_text.count(i) / len(filtered_text)))
    h = 0
    for i in frequency:
        if i != 0:
            h += i * math.log2(1 / i)
    return h


def decrypt_text(temp_keys, filename):
    encrypted_bigramms = convert_bigrams(find_popular_bigramms(read_text_from_file(file), 1), 1)
    global russ_letters
    for k in temp_keys:
        back_a = euclid_algorithm(k[0], (len(russ_letters))**2)
        b = k[1]
        if back_a != 0:
            x = []
            for i in encrypted_bigramms:
                x.append(pow(back_a*(i - b), 1, len(russ_letters)**2))
            y = ""
            for i in range(len(x)):
                y += russ_letters[(x[i]//31)]
                y += russ_letters[(x[i] - (x[i]//31)*31)]
            if entropy_func(y) <= 4.459204208751:
                print("key =", k)
                print("Entropy of text:", entropy_func(y))
                print("Text: ", y)


if __name__ == '__main__':
    file = "19.txt"
    russ_letters = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
    my_keys = find_key(file)
    decrypt_text(my_keys, file)





