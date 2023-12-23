import argparse;
import string

class otp:
    def __init__(self, argv):
        return ;

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

def exec():
    args = init_args()
    if (args.generate is not None):
        with open(args.generate, "r") as f:
            byte = f.read()
            isHex = all(c in string.hexdigits for c in byte)
            if (not isHex):
                print("The key is not in hexadecimal")
                exit(1)
            if (len(byte) != 64):
                print("The key is not 64 character long")
                exit(1)
                
    elif (args.key is not None):
        print("hello")

if __name__ == '__main__':
    exec()