import re


def read_text_from_file(your_filename):
    with open(your_filename, "r", encoding='UTF-8') as f:
        unfiltered_text_from_file = f.read()
    filtered_text_from_file = unfiltered_text_from_file.lower()
    filtered_text_from_file = re.sub(r'[^а-я]', '', filtered_text_from_file).replace('ё', 'e')
    return filtered_text_from_file


def correspondence_index(text):
    global russ_letters
    counter = 0
    for i in russ_letters:
       counter += text.count(i)*(text.count(i)-1)
    index = counter/((len(text)) * ((len(text)) - 1))
    return index


def encrypt_text(text_to_encrypt):
    global russ_letters
    key = input("Enter your key: ")
    encrypted_text = ""
    for i in range(len(text_to_encrypt)):
        encrypted_text += russ_letters[pow((russ_letters.find(text_to_encrypt[i]) + russ_letters.find(key[pow(i, 1, len(key))])), 1, len(russ_letters))]
    print("Clear Text:", text_to_encrypt)
    print("Index =", correspondence_index(text_to_encrypt))
    print("Key:", key)
    print("Encrypted text:", encrypted_text)
    print("Index =", correspondence_index(encrypted_text))
    return encrypted_text


def guess_key(encrypted_text):
    global russ_letters
    average_value = 0
    sorted_letters = "оеаинтслвркдмупяьгыбзчйжшхюцэщф"
    theoretical_value = 0.0553
    my_dict = {}
    for n in range(2, 31):
        for j in range(0, n):
            y = [encrypted_text[i:i + 1] for i in range(j, len(encrypted_text), n)]
            average_value += correspondence_index(y)
        my_dict[n] = average_value/n
        average_value = 0
    length_of_key = list(sorted(my_dict.items(), key=lambda x: abs(x[1] - theoretical_value))[0])[0]
    print("The length of key =", length_of_key)

    key = ''
    for j in range(0, length_of_key):
        y = [encrypted_text[i:i + 1] for i in range(j, len(encrypted_text), length_of_key)]
        often_let = 0
        for i in y:
            if often_let < y.count(i):
                often_let = y.count(i)
                letter = i
        key += russ_letters[pow(russ_letters.find(letter) - russ_letters.find(sorted_letters[0]), 1, len(russ_letters))]
    print("Your key is:", key)
    return key


def decrypt_text(text_to_decrypt, key_to_encrypt):
    global russ_letters
    decrypted_text = ""
    for i in range(len(text_to_decrypt)):
        decrypted_text += russ_letters[pow((russ_letters.find(text_to_decrypt[i]) - russ_letters.find(key_to_encrypt[pow(i, 1, len(key_to_encrypt))])), 1, len(russ_letters))]
    print("This is your clear text:", decrypted_text)
    open("decrypted.txt", "w", encoding='UTF-8').write(decrypted_text)


def main():
    while True:
        print("\nWhat u want to do:\n"
              "(1) encrypt text\n"
              "(2) decrypt text\n"
              "(0) exit")
        answer_of_user = int(input())
        if answer_of_user == 1:
            some_text = read_text_from_file("to_encrypt.txt")
            encrypt_text(some_text)
        if answer_of_user == 2:
            some_text = read_text_from_file("to_decrypt.txt")
            decrypt_text(some_text, guess_key(some_text))
        if answer_of_user == 0:
            break


if __name__ == '__main__':
    russ_letters = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    main()



