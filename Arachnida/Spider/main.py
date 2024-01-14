import argparse
import requests
from lxml import html
import os
import copy
from urllib.parse import urlsplit, urlparse

supported_extensions = ["png", "jpg", 'jpeg', 'gif', 'bmp']
already_visited = []
already_downloaded = []

class Spider:
    base_url : str = "";
    deep_lvl : int = 1;
    verbose: bool = False;
    path: str = "data/";

    def __init__(self, args):
        self.base_url = args.URL
        if (not self.base_url.endswith('/')):
            self.base_url = self.base_url + '/'
        if (args.recursive == True):
            self.deep_lvl = 5
        if (args.length is not None):
            self.deep_lvl = args.length
        elif (args.recursive == False):
            self.deep_lvl = 0
        self.verbose = args.verbose
        if (args.path != None):
            self.path = args.path
            if (not self.path.endswith("/")):
                self.path = self.path + "/"

    def make_request(self, url):
        response = requests.get(url, timeout=3);
        if (response.status_code != 200):
            raise ValueError("Url not valid");
        return response.content
        
    def increm_name(self, pathname):
        i = 1
        filename, extensions = os.path.splitext(pathname)
        while os.path.exists(filename + "_" + str(i) + extensions):
            i = i + 1
        return filename + "_" + str(i) + extensions;

    
    def download_images(self, image_list):
        for image in image_list:
            try: 
                image_name = os.path.basename(image)
                if (not image.endswith(tuple(supported_extensions))):
                    continue
                if (image in already_downloaded):
                    continue
                if (image.startswith('//')):
                    image = "https:" + image
                elif (image.startswith('/')):
                    image = urlsplit(self.base_url).scheme + "://" + urlsplit(self.base_url).netloc + image
                image_content = self.make_request(image);
                if (self.verbose):
                    print("New image:", image)
                isExist = os.path.exists(self.path)
                if (not isExist):
                    os.makedirs(self.path)
                pathname = self.path + image_name;
                if (os.path.exists(pathname)):
                    pathname = self.increm_name(pathname)
                with open(pathname, "wb") as f:
                    f.write(image_content)
                already_downloaded.append(image)
            except ValueError as e:
                print("Invalid image" , e)

    def transfo_link(self, link):
        url = urlsplit(link)
        if (url.scheme == "" and url.path.startswith("/")):
            return urlsplit(self.base_url).scheme + "://" + urlsplit(self.base_url).netloc + url.path
        if (url.scheme + "://" + url.netloc + "/" != self.base_url):
            raise ValueError();
        return link


    def recurse_scrap(self, url, deep_lvl):
        already_visited.append(url)
        try:
            page_content = self.make_request(url);
            tree = html.fromstring(page_content)
            b = tree.xpath("//img/@src")
            self.download_images(b);
            if (deep_lvl == 0):
                return ;
            a = tree.xpath("//a/@href")
            for link in a:
                try: 
                    cleaned_link = self.transfo_link(link)
                except:
                    continue
                if (cleaned_link not in already_visited):
                    if (self.verbose):
                        print("New url: ", cleaned_link)
                    self.recurse_scrap(cleaned_link, deep_lvl - 1)
        except ValueError as e:
            print("Error invalid url")
            return ;



def init_args():
    parser = argparse.ArgumentParser(
                    prog='spider',
                    description='A program that crawl the url specified and save all image found in a directory',
                    epilog='Made with <3 by hrecolet')
    parser.add_argument('URL')
    parser.add_argument('-r', '--recursive', action='store_true')
    parser.add_argument('-l', '--length', type=int)
    parser.add_argument('-p', '--path')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()
    return args

def exec():
    args = init_args()
    spider_instance = Spider(args)
    spider_instance.recurse_scrap(spider_instance.base_url, copy.deepcopy(spider_instance.deep_lvl))
    print("Downloaded", len(already_downloaded))
    print("URL visited:", len(already_visited))

if __name__ == '__main__':
    exec()
