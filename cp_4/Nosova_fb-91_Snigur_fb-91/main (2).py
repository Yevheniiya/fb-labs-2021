import random

def el_to_power(el, power, mod):  # Схема Горнера
    result = 1
    binary_power = bin(power)[2:]
    for i in range(len(binary_power)):
        if binary_power[i] != '0':
            result = (el * result) % mod
        if i == len(binary_power) - 1:
            break
        result = (result * result) % mod
    return result


def inverse_of_el(el, mod):  # Знаходження оберненого та нсд  gcd = el * v + u * mod
    if el == 0:
        return 0
    if mod == 0:
        return el, 1, 0
    gcd, u, v = inverse_of_el(mod, el % mod)
    return gcd, v, u - (el // mod) * v


def prime_check(number_to_check):  # Імовірністний тест Ферма
    accuracy = 100  # Обираєм точніть
    for i in range(accuracy):  # крок 0 і 1 починаєм ітеруватись до вказаної ймовіносі
        x = random.randint(2, number_to_check)  # Обираєм незалежне випадкове число
        gcd = inverse_of_el(x, number_to_check)[0]  # Знаходим НСД за алгоритмом Евкліда
        if gcd > 1:  # Якщо більше 1 то не просте
            return False
        else:  # Інакше крок 2
            value = el_to_power(x, number_to_check - 1, number_to_check)  # Рахуєм х^(p-1) mod p
            if value == 1:  # Якщо одиниця то р - псевдопросте за х і переходим до наступної ітерації
                continue
            else:  # інакше не псевдо просте, а отже складне
                return False
    return True  # Якщо пройшли всі провірки то число просте


def generate_prime(num_len_in_bit):  # Генерація простих чисел вказаної довжини в бітах
    minimum = pow(2, num_len_in_bit)
    maximum = pow(2, num_len_in_bit + 1) - 1
    prime = random.randint(minimum, maximum)
    if prime % 2 != 1:
        prime += 1
    while not prime_check(prime):
        prime += 2
    return prime


def generate_keys(key_length):  # Генерація ключів вказаної довжини в бітах
    minimum = pow(2, key_length)
    maximum = pow(2, key_length + 1) - 1
    p = generate_prime(key_length // 2)
    q = generate_prime(key_length // 2)
    n = p * q
    fi_n = (p - 1) * (q - 1)
    pub_exp = pow(2, 16) + 1
    d = inverse_of_el(pub_exp, fi_n)[1] % fi_n
    public_key = [n, pub_exp]
    private_key = [d, p, q]
    return [public_key, private_key]


def to_decrypt(Cipher_text, private_key, public_mod):  # Функція розшифрування
    Open_text = el_to_power(Cipher_text, private_key, public_mod)
    return Open_text


def to_encrypt(Open_text, public_exp, public_mod):  # Функція шифрування
    Cipher_text = el_to_power(Open_text, public_exp, public_mod)
    return Cipher_text


def to_sign(Open_text, private_key, public_mod):  # Функція цифрового підпису
    Signature = to_encrypt(Open_text, private_key, public_mod)
    return Signature


def to_verify(Open_text, Signature, public_exp, public_mod):  # Функція перевірки цифрового підпису
    if Open_text == to_decrypt(Signature, public_exp, public_mod):
        return True
    else:
        return False


# Функція відправлення (формує повідомлення що буде відправлене)
def to_send(Open_text, server_public_mod, server_public_exp, my_private_key, my_public_mod):
    Signature = to_sign(Open_text, my_private_key, my_public_mod)
    Cipher_text = to_encrypt(Open_text, server_public_exp, server_public_mod)
    Cipher_signature = to_encrypt(Signature, server_public_exp, server_public_mod)
    return [hex(Cipher_text)[2:], hex(Cipher_signature)[2:]]


# Функція отримання (оброблює отримане повідомлення, розшифровуючи його та перевіряючи його піддліність і )
def to_receive(Cipher_text, Cipher_signature, server_public_mod, server_public_exp, my_public_mod, my_private_key):
    Cipher_signature = int(Cipher_signature, 16)
    Cipher_text = int(Cipher_text, 16)
    Open_text = to_decrypt(Cipher_text, my_private_key, my_public_mod)
    Signature = to_decrypt(Cipher_signature, my_private_key, my_public_mod)
    to_check = to_verify(Open_text, Signature, server_public_exp, server_public_mod)
    if to_check:
        return [True, Open_text]
    else:
        return [False, Open_text]


[[Alice_n, Alice_e], [Alice_d, Alice_p, Alice_q]] = generate_keys(1024)  # Alice's keys
[[Bob_n, Bob_e], [Bob_d, Bob_p, Bob_q]] = generate_keys(1024)  # Bob's keys

print("Keys of Alice:")
print(f"n is: {hex(Alice_n)[2:]}")
print(f"e is: {hex(Alice_e)[2:]}")
print(f"fi(n) is: {hex(((Alice_p-1)*(Alice_q-1)))[2:]}")
print(f"d is: {hex(Alice_d)[2:]}")
print(f"p is: {hex(Alice_p)[2:]}")
print(f"q is: {hex(Alice_q)[2:]}")
print("Keys of Bob:")
print(f"n is: {hex(Bob_n)[2:]}")
print(f"e is: {hex(Bob_e)[2:]}")
print(f"fi(n) is: {hex(((Bob_p - 1)*(Bob_q - 1)))[2:]}")
print(f"d is: {hex(Bob_d)[2:]}")
print(f"p is: {hex(Bob_p)[2:]}")
print(f"q is: {hex(Bob_q)[2:]}")

# encryption and decryption (Alice sends message to Bob)
open_text = random.randint(123, 99999999)
print(f"open text Alice wants to send: {open_text}")
cipher_text = to_encrypt(open_text, Bob_e, Bob_n)
print(f"Encrypted text with Bob's public key: {cipher_text}")
decrypted_text = to_decrypt(cipher_text, Bob_d, Bob_n)
print(f"The text Bob received after decryption with his private key: {decrypted_text}")


# signing and verifying (Alice sends signed text to Bob)

print(f"\n\n\nopen text Alice wants to send: {open_text}")
signed_text = to_send(open_text, Bob_n, Bob_e, Alice_d, Alice_n)
print("encrypted msg is:" + signed_text[0] + "\nsignature is: " + signed_text[1])
# B received signed_msg and knows e and n
[check, k] = to_receive(signed_text[0], signed_text[1], Alice_n, Alice_e, Bob_n, Bob_d)
if check:
    print("Signature is valid\nencrypted msg is: " + str(k))
else:
    print("invalid signature")


serv_public_mod = 148346691641360228269889924052736000522012383073872477471487393579573336538272653144469629890498930894743775145635448512467051608573214757454577973448145601806954215786381800193292823475590280148622353816833611047020330327248216359523382842632814225741604775891863035054818812563283402969340442028816299190899
serv_public_exp = 65537

open_text = random.randint(123, 99999999)
print(f"open text Alice wants to send:", open_text)
signed_text = to_send(open_text, serv_public_mod, serv_public_exp, Alice_d, Alice_n)

print("key", signed_text[0])
print("signature", signed_text[1])
print("modulus", hex(Alice_n)[2:])
print("publicExponent", hex(Alice_e)[2:])
