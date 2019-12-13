import random
import base64
import hashlib
import os
if os.name == 'nt':
    from Cryptodome import Random
    from Cryptodome.Cipher import AES
    from Cryptodome.Util.Padding import pad, unpad
else:
    from Crypto import Random
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad


# генератор простых чисел
class Primer(object):
    def __init__(self, p, q):
        self.primes = [i for i in range(p, q) if is_prime(i)]

    def get_prime(self):
        return random.choice(self.primes)


# AES класс для шифрования (в данной лабораторке пофиг какой, но пусть будет AES)
class AESCipher(object):
    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = pad(raw, 16)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[AES.block_size:]), 16).decode('utf-8')


def is_prime(n):
    d = 2
    while d * d <= n and n % d != 0:
        d += 1
    return d * d > n
