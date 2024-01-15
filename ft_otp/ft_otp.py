import argparse;
import string
import hmac
import base64;
import datetime
import time
from cryptography.fernet import Fernet
import base64
import pyotp
    
def init_args():
    parser = argparse.ArgumentParser(
                    prog='ft_otp',
                    description='A program based on TOTP algorithm that generate a new password from an hexadecimal key stored in a file',
                    epilog='Made with <3 by hrecolet')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-g', '--generate')
    group.add_argument('-k', '--key')
    args = parser.parse_args()
    return args

def check_generate(args):
    with open(args.generate, "r") as f:
        byte = f.read()
        isHex = all(c in string.hexdigits for c in byte)
        if (not isHex):
            print("The key is not in hexadecimal")
            exit(1)
        if (len(byte) != 64):
            print("The key is not 64 character long")
            exit(1)
        with open("./hash.key", "w+b") as f:
            key = f.read()
            if (key.decode('utf-8') == ""):
                key = Fernet.generate_key()
                f.write(key);
            fernet = Fernet(key)
            hash = fernet.encrypt(byte.encode())
            return hash


def low_order_4_bits(val):
    return val & 0b1111


def last_31_bits(p):
    res = bytearray()
    res.append(p[0] & 0x7F)
    for b in p[1:]:
        res.append(b & 0xFF)
    return res


def DT(hash_string):
    offset = low_order_4_bits(hash_string[19])
    p = hash_string[offset:offset+4]
    return last_31_bits(p)


def hotp(key, code):
    counter_bytes = code.to_bytes(8, byteorder='big')
    hs_hmac = hmac.new(key, counter_bytes, "sha1")
    hs = hs_hmac.digest()
    s_bits = DT(hs)
    s_num = int(s_bits.hex(), 16)
    return s_num % 10 ** 6

def totp(key, intervale = 30):
    s_since_epoch = time.mktime(datetime.datetime.now().timetuple())
    time_steps = int(s_since_epoch / intervale)
    return hotp(key, time_steps)

def exec():
    args = init_args()
    if (args.generate is not None):
        key = check_generate(args)
        file = open('ft_otp.key', 'wb')
        file.write(key)
    elif (args.key is not None):
        file = open(args.key, 'r')
        key_hash = file.read()
        with open("hash.key", "r") as f:
            master_key = f.read()
            fernet = Fernet(master_key)
            key = base64.b32encode(fernet.decrypt(key_hash))
            code = totp(base64.b32decode(key))
            true_otp = pyotp.TOTP(key).now()
            print("True OTP:", true_otp)
            print("Ft_OTP:", str(code).zfill(6))

if __name__ == '__main__':
    exec()