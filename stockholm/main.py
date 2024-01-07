import argparse
import os
from cryptography.fernet import Fernet

program_version = 'Version 1.0'
supported_extensions_path = "./supported_extensions"
# infection_path = f"{os.getenv('HOME')}/infection/"
infection_path = "./infection/"
extensions = ".ft"
key_file_path = "./encryption_key.key"

class Stockholm:
    isSilent = False
    supported_extensions = []
    fernet_instance = None

    def __init__(self, args):
        if (args.silent == True):
            self.isSilent = True;
        try:
            file = open(supported_extensions_path, "r")
            extensions = file.read()
            self.supported_extensions = extensions.replace(' ', '').split('\n')
        except:
            print("Extensions file not found!")
            exit(1);
    

    def reverse_infection(self):
        file = open(key_file_path, 'r');
        key = file.read();
        self.fernet = Fernet(key);
        return ;
    
    def generate_key(self):
        file = open(key_file_path, 'a+b');
        file.seek(0)
        old_key = file.read();
        file.seek(0)
        if (old_key.decode() == ""):
            key = Fernet.generate_key()
            file.write(key)
            return key
        return old_key

    def infect(self):
        key = self.generate_key()
        self.fernet = Fernet(key)
        return ;



def init_args():
    parser = argparse.ArgumentParser(
                    prog='stockholm',
                    description='A program that imitate a ransomware, created only for educationnal purpose',
                    epilog='Made with <3 by hrecolet')
    parser.add_argument('-v', '--version', action='store_true')
    parser.add_argument('-s', '--silent', action='store_true')
    parser.add_argument('-r', '--reverse', type=str)
    args = parser.parse_args()
    return args

def exec():
    args = init_args()
    if (args.version):
        print(program_version)
        return ;
    
    stockholm = Stockholm(args);
    if (args.reverse):
        stockholm.reverse_infection()
    else:
        stockholm.infect()
        

if __name__ == '__main__':
    exec()