import re
import math
from prettytable import PrettyTable


def filter_text_from_file(your_filename, var_of_space):
    with open(your_filename, "r", encoding='UTF-8') as f:
        unfiltered_text_from_file = f.read()
    filtered_text_from_file = unfiltered_text_from_file.lower()
    filtered_text_from_file = re.sub(r'[^А-Яа-я\s]', '', filtered_text_from_file).replace('ъ', 'ь').replace('ё', 'e')
    filtered_text_from_file = filtered_text_from_file.split()
    if var_of_space:
        filtered_text_from_file = "".join(filtered_text_from_file)
    else:
        filtered_text_from_file = " ".join(filtered_text_from_file)
    return filtered_text_from_file


def frequency_of_letter(filtered_text):
    letters_and_frequency = {}
    russ_letters = 'абвгдежзийклмнопрстуфхцчшщыьэюя '
    for i in russ_letters:
        letters_and_frequency[i] = (filtered_text.count(i) / len(filtered_text))
    temp_list = list(letters_and_frequency.items())
    temp_list.sort(key=lambda i: i[1], reverse=True)
    for el in temp_list:
        print("Frequency of letter ", el[0], ':', el[1])
    return letters_and_frequency.values()


def biggrams_func(filtered_text, var_of_biggrams):
    if(len(filtered_text)%2!=0):
        filtered_text = filtered_text + "a"
    if var_of_biggrams:
        bigram_of_text = [filtered_text[i:i+2] for i in range(0, len(filtered_text), 2)]
    else:
        bigram_of_text = [filtered_text[i:i + 2] for i in range(len(filtered_text) - 1)]
    #print("Bigrams: ", bigram_of_text)
    print("Number of all bigrams", len(bigram_of_text))
    frequency_of_bigrams = {}
    for bg in bigram_of_text:
        if bg not in frequency_of_bigrams:
            frequency_of_bigrams[bg] = bigram_of_text.count(bg) / len(bigram_of_text)
            #print("Frequency of bigram ", bg, "=", bigram_of_text.count(bg) / len(bigram_of_text))
    list_of_freq_and_letters = list(frequency_of_bigrams.items())
    table_of_freq = PrettyTable()
    print("Number of unique bigrams", len(list_of_freq_and_letters))
    number_of_rows = int(len(list_of_freq_and_letters) ** (1/2))
    for i in range(number_of_rows):
        table_of_freq.add_row(list_of_freq_and_letters[number_of_rows*i:number_of_rows*(i+1)])
    with open('bg.txt', 'w') as fp:
        table = table_of_freq.get_string()
        fp.write(table)
    list_of_freq = []
    for i in list_of_freq_and_letters:
        list_of_freq.append(i[1])
    return list_of_freq


def entropy_func(some_frequencies, n):
    h = 0
    #print("Length = ", len(some_frequencies))
    for i in some_frequencies:
        if i != 0:
            h += i/n * math.log2(1 / i)
    r = 1 - h/5
    print("Entropy = ", h)
    print("Redundancy = ", r)


def main():
    print("Enter your file to read ")
    name_of_file = input()
    while True:
        print("\nWhat u want to do:\n"
              "(1) monograms without space \n"
              "(2) monograms with space\n"
              "(3) biggrams without space\n"
              "(4) biggrams with space\n"
              "(5) biggrams with crossing without space\n"
              "(6) biggrams with crossing with space\n"
              "(0) exit")
        answer_of_user = int(input())
        if answer_of_user == 1:
            filter_text = filter_text_from_file(name_of_file, 1)
            print("Length of text ", len(filter_text))
            letters_freq = frequency_of_letter(filter_text)
            entropy_func(letters_freq, 1)
        if answer_of_user == 2:
            filter_text = filter_text_from_file(name_of_file, 0)
            print("Length of text ", len(filter_text))
            letters_freq = frequency_of_letter(filter_text)
            entropy_func(letters_freq, 1)
        if answer_of_user == 3:
            filter_text = filter_text_from_file(name_of_file, 1)
            biggrams_freq = biggrams_func(filter_text, 1)
            entropy_func(biggrams_freq, 2)
        if answer_of_user == 4:
            filter_text = filter_text_from_file(name_of_file, 0)
            biggrams_freq = biggrams_func(filter_text, 1)
            entropy_func(biggrams_freq, 2)
        if answer_of_user == 5:
            filter_text = filter_text_from_file(name_of_file, 1)
            biggrams_freq = biggrams_func(filter_text, 0)
            entropy_func(biggrams_freq, 2)
        if answer_of_user == 6:
            filter_text = filter_text_from_file(name_of_file, 0)
            biggrams_freq = biggrams_func(filter_text, 0)
            entropy_func(biggrams_freq, 2)
        if answer_of_user == 0:
            break


if __name__ == "__main__":
    main()