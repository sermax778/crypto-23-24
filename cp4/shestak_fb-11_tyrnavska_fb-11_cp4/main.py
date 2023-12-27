import random
import hashlib


#############################
# 1 task


# додаткова ф-ція, піднесення до степеня за модулем
# використовується бінарний метод
def power(x, y, p):  # повертає (x^y) % p
    res = 1

    x = x % p
    while y > 0:
        if y & 1:
            res = (res * x) % p

        y = y >> 1  # y = y/2
        x = (x * x) % p

    return res


###
# Test power()
#
# print(power(50, 43, 17))
# print((50**43)%17)


# ця ф-ція використовується для всіх ітерацій k
def m_test(d, n):
    a = 2 + random.randint(1, n - 4)
    x = power(a, d, n)

    if x == 1 or x == n - 1:
        return True

    while d != n - 1:
        x = (x * x) % n
        d *= 2

        if x == 1:
            return False
        if x == n - 1:
            return True

    return False


# використовуючи попередню функцію перевіряє чи є число простим
# також можна вказати точність (k)
def is_prime(n, k):
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True

    d = n - 1
    while d % 2 == 0:
        d //= 2

    for i in range(k):
        if not m_test(d, n):
            return False

    return True


###
# Test is_prime()
#
# print(is_prime(96, 20))


# функція для знаходження випадкового простого числа в діапазоні (або по кількості бітів!)
def random_prime(start=None, end=None, bits=None):
    if (start is None or end is None) and bits is None:
        raise ValueError("Необхідно вказати або діапазон, або кількість.")

    if end is not None and start is not None:
        while True:
            num = random.randint(start, end)
            if is_prime(num, 15):
                return num

    if bits is not None:
        while True:
            num = random.getrandbits(bits)
            if is_prime(num, 15):
                return num

# Примітка*
# Якщо використовувати пробне ділення,
# то алгоритм починає працювати В РАЗИ довше,
# тому було прийняте рішення не застосовувати пробне ділення


###
# Test random_prime()
#
# some = random_prime(100000000, 20000000000000)
# some = random_prime(bits=256)
# print(some)
# print(is_prime(some, 20))


#############################
# 2 task


def get_keys():
    p = 1
    q = 1
    p1 = 0
    q1 = 0

    while True:
        if p*q <= p1*q1:
            return p, q, p1, q1

        p = random_prime(bits=256)
        q = random_prime(bits=256)
        p1 = random_prime(bits=256)
        q1 = random_prime(bits=256)


p, q, p1, q1 = get_keys()


###
# Test get_keys()
#
# print(p*q)
# print(p1*q1)
# print(len(str(p*q)))
# print(len(str(p1*q1)))


#############################
# 3 task

# математичні ф-ції з попередньої лаби

# Функція для розширеного алгоритму Евкліда
def extended_euclid(a, b):
    # Повертає d=НСД(x,y) і x, y такі, що ax + by = d
    if b == 0:
        return a, 1, 0
    d, x, y = extended_euclid(b, a % b)
    return d, y, x - (a // b) * y


# Функція для знаходження оберненого a за модулем m
def mod_inverse(a, m):
    gcd, x, y = extended_euclid(a, m)
    if gcd != 1:
        return None
    else:
        return x % m if x < 0 else x


# Функція для розв'язування порівнянь (лінійних конгруенцій)
def solve_linear_congruence(a, b, m):
    gcd, x, y = extended_euclid(a, m)
    if b % gcd != 0:
        return None
    inverse = mod_inverse(a // gcd, m // gcd)
    x0 = (inverse * (b // gcd)) % (m // gcd)

    ans = []
    for i in range(gcd):
        solution = (x0 + i * (m // gcd)) % m
        ans.append(solution)

    return ans


# ф-ція для генерації пар ключів за двома простими числами
def GenerateKeyPair(p, q):
    n = p * q
    fi_n = (p - 1) * (q - 1)  # ф(n)

    e = 65537

    # секретний ключ d
    d = mod_inverse(e, fi_n)

    # відкритий і закритий ключі
    public_key = (e, n)
    private_key = (d, p, q)

    return public_key, private_key


# створення пар ключів для користувача A та B
user_A = GenerateKeyPair(p, q)
user_B = GenerateKeyPair(p1, q1)

###
# Test pairs of keys
# print(user_A)
# print(user_B)


#############################
# 4 task


# шифрує повідомлення
def encrypt(message, public_key):
    e, n = public_key
    encrypted_message = power(message, e, n)

    return encrypted_message


# розшифровує повідомлення
def decrypt(encrypted_message, private_key):
    d, p, q = private_key
    n = p * q
    decrypted_message = power(encrypted_message, d, n)

    return decrypted_message


# створює підпис
def create_signature(message, private_key):
    d, p, q = private_key
    n = p * q
    signature = power(message, d, n)

    return signature


# перевіряє автентичність повідомлення порівнюючи підписи (виводить True або False)
def verify_signature(signature, public_key, message):
    e, n = public_key
    decrypted_signature = power(signature, e, n)

    return message == decrypted_signature


# "розпакуємо" ключі користувачів для зручності
public_key_A, private_key_A = user_A
public_key_B, private_key_B = user_B

print('Публічний ключ:', public_key_A)
print('Приватиний ключ:', private_key_A)


# ввід якогось повідомлення
message = random_prime(bits=128)

print('Відкрите повідомлення:')
print(message)

# перевіримо шифрування повідомлень для абонентів A та B
enc_message_A = encrypt(message, public_key_A)

print("Зашифроване повідомлення:")
print(enc_message_A)

# перевіримо розшифрування для абонентів A та B
dec_message_A = decrypt(enc_message_A, private_key_A)

print("Розшифроване повідомлення:")
print(dec_message_A)

# створимо підпис для повідомлення
signature_A = create_signature(message, private_key_A)

print("Цифровий підпис:")
print(signature_A)

# перевіримо підпис
verified_signature_A = verify_signature(signature_A, public_key_A, message)

print(f"Повідомлення є автентичним - {verified_signature_A}")


# 5 task
def send_key(k, key, private_key):
    s = create_signature(k, private_key)
    s1 = encrypt(s, key)
    k1 = encrypt(k, key)

    print(f's - {s}\ns1 - {s1}\nk1 - {k1}')

    return k1, s1


def receive_key(k1, s1, key, private_key):
    k = decrypt(k1, private_key)
    s = decrypt(s1, private_key)

    print(f'k - {k}\ns - {s}')

    return verify_signature(s, key, k)


# create new message for protocol
k = random_prime(bits=128)
print(f'k - {k}')

k1, s1 = send_key(k, public_key_B, private_key_A)
print(receive_key(k1, s1, public_key_A, private_key_B))
