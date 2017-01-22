from Crypto.Cipher import AES
from Crypto.Protocol import KDF
import binascii

# Blocksize by default is 16 bytes for AES-128.
BLOCKSIZE = 16

NUM_REPO = dict(
    dict({i: str(i) for i in range(10)}).items() +
    dict({10: 'a', 11: 'b', 12: 'c', 13: 'd',
          14: 'e', 15: 'f', 16: 'g'}).items()
)

# Crypto.get_random_bytes()
SALT = '_\x94\xdb\xbd\xd8\xdd?5\xff\xb5\xe1\x9d\xbe\n\x16\xc2'
IV = '\x03\x0c\x06\xf0B\xdb\xcbv!0\xe4\xea"\xc3;-'


def base_10_to_b(decimal, b):
    new_num_string = ''
    current = decimal
    while current != 0:
        current, remainder = divmod(current, b)
        if 26 > remainder > 9:
            remainder_string = NUM_REPO[remainder]
        else:
            remainder_string = str(remainder)
        new_num_string = remainder_string + new_num_string
    return new_num_string


def base_b_to_10(number, b):
    result = 0
    number = list(str(number))
    number.reverse()
    for i in range(len(number)):
        for j in NUM_REPO:
            if number[i] == NUM_REPO[j]:
                result += int(j) * b ** int(i)
    return result


# def base_b_to_d(number, b, d):
#     return base_10_to_b(base_b_to_10(number, b), d)


def gen_key(password, salt, dkLen=BLOCKSIZE):
    return KDF.PBKDF2(str(password), salt, dkLen=BLOCKSIZE)


def pad(plaintext):
    topad = BLOCKSIZE - (len(plaintext) % BLOCKSIZE)
    padded = str(plaintext + bytearray([topad] * topad))
    return padded


def unpad(padded_plaintext):
    bytestring = bytearray(padded_plaintext)
    padding_char = bytestring[-1]
    plaintext = str(bytestring[: len(bytestring) - padding_char])
    return plaintext


def encrypt(text, password, salt=SALT, IV=IV):
    padded_text = pad(text)
    key = gen_key(password, salt)
    cipher = AES.AESCipher(key, AES.MODE_CBC, IV=IV)
    ciphertext_b256 = cipher.encrypt(padded_text)
    ciphertext_b16 = binascii.hexlify(bytearray(ciphertext_b256))
    ciphertext_b10 = base_b_to_10(ciphertext_b16, 16)
    return ciphertext_b10


def decrypt(ciphertext, password, salt=SALT, IV=IV):
    ciphertext_b16 = base_10_to_b(ciphertext, 16)
    ciphertext_original = binascii.unhexlify(ciphertext_b16)
    key = gen_key(password, salt)
    cipher = AES.AESCipher(key, AES.MODE_CBC, IV=IV)
    padded_plaintext = cipher.decrypt(ciphertext_original)
    return unpad(padded_plaintext)
