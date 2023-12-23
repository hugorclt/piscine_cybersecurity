import requests
import argparse;

supported_extensions = ["png", "jpg", 'jpeg', 'gif', 'bmp']

def get_url_site(str: str, decal: int ):
    first_index = str.find("href=\"", decal) + 6;
    scnd_index = str.find("\"", first_index);
    return str[first_index:scnd_index];

def get_url_img(str: str, decal: int ):
    first_index = str.find("src=\"", decal) + 5;
    scnd_index = str.find("\"", first_index);
    return str[first_index:scnd_index];

def init_args():
    parser = argparse.ArgumentParser(
                    prog='spider',
                    description='A program that crawl the url specified and save all image found in a directory',
                    epilog='Made with <3 by hrecolet')
    parser.add_argument('URL')
    parser.add_argument('-r', '--recursive', action='store_true')
    parser.add_argument('-l', '--length')
    parser.add_argument('-p', '--path')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()
    return args

class Spider:
    base_url = ""
    already_visited = []
    path_to = ""
    verbose = False

    def __init__(self, base_url, path_to, verbose) -> None:
        if (not base_url.endswith('/')):
            base_url += '/'
        self.base_url = base_url
        self.path_to = path_to
        self.verbose = verbose

    def download_image(self, url_img):
        if (len(url_img) > 0):
            if (url_img.startswith('//')):
                url_img = "https:" + url_img
            elif (not (url_img.startswith('http://') or url_img.startswith('https://'))):
                url_img = self.base_url + url_img
            if (not url_img.endswith(tuple(supported_extensions))):
                return ;
            self.verbose and print("DOWNLOADING IMAGE:\n" + url_img)
            image_res = requests.get(url_img);
            image_name = url_img[url_img.rfind('/') + 1:len(url_img)]
            with open("data/" + image_name, "wb") as f:
                f.write(image_res.content)

    def clean_url(self, url):
        if (url.endswith('.html') or url.endswith('.php') or url.endswith('.py')):
            last_slash = url.find("/")
            if (last_slash != -1):
                url = url[0:url.rfind('/')]
            else:
                return ""
        if (not url.endswith('/')):
            url += "/"
        return url
    
    def is_in_script(self, file, indexToCheck):
        find_open = file.rfind("<script", 0, indexToCheck);
        if (find_open > file.rfind("</script>", 0, indexToCheck)):
            return True
        return False

    def recurse_scrap(self, url, deep_lvl):
        if (deep_lvl <= 0):
            return ;
        site_bytes = requests.get(url);
        site_str = str(site_bytes.content)
        indexStart = 0;
        while (indexStart != -1):
            indexOfImg = site_str.find("<img", indexStart);
            indexOfSite = site_str.find("<a", indexStart);
            firstIsImage = indexOfImg < indexOfSite;
            if (indexOfImg == -1):
                firstIsImage = False
            if (indexOfSite == -1):
                firstIsImage = True
            if (indexOfSite == -1 and indexOfImg == -1):
                return ;
            if (firstIsImage == True and not self.is_in_script(site_str, indexOfImg)):
                indexStart = indexOfImg
                img = get_url_img(site_str, indexStart);
                self.download_image(img)
            if (firstIsImage == False and not self.is_in_script(site_str, indexOfSite)):
                indexStart = indexOfSite
                url_found = get_url_site(site_str, indexStart);
                if (not (url_found.startswith('https') or url_found.startswith('http') or url_found in self.already_visited)):
                    self.already_visited.append(url_found)
                    new_url = self.clean_url(url_found)
                    final_url = ""
                    if (new_url.startswith('/')):
                        final_url = self.base_url + new_url[1:]
                    else:
                        final_url = url + "/" + new_url
                    self.verbose and print("URL FOUND:\n" + final_url[:-1])
                    self.recurse_scrap(final_url[:-1], deep_lvl - 1)
            if (indexStart != -1):
                indexStart += 1
        return ;

def exec():
    args = init_args()
    base_url = args.URL
    recursion_lvl = int(args.length)
    if (recursion_lvl == None):
        recursion_lvl = 5
    if (args.recursive == False):
        recursion_lvl = 1
    destination = args.path
    spider = Spider(base_url, destination, args.verbose)
    spider.recurse_scrap(base_url, recursion_lvl);
    return ;

if __name__ == '__main__':
    exec()
