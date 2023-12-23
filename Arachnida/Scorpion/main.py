import sys
import requests
from PIL import Image
from io import BytesIO
from PIL.ExifTags import TAGS

supported_extensions = ["png", "jpg", 'jpeg', 'gif', 'bmp']

class Scorpion:
    image_url = []

    def __init__(self, argv):
        self.image_url = argv

    def _parse_exif(self, url):
        try:
            image_http_res = requests.get(url)
            img = Image.open(BytesIO(image_http_res.content))
            exif_data = img._getexif()
            img.close()
            self._display_exif_data(exif_data)
        except:
            print("An error occured during the request, wrong url?")

            
    def _display_exif_data(self, exif_info):
        if exif_info is not None:
            for tag, value in exif_info.items():
                print(f'Tag: {TAGS[tag]}, Value: {value}')
        else:
            print('Aucune donnée EXIF trouvée.')

    def launch(self):
        for url in self.image_url:
            self._parse_exif(url)

def check_ext(args):
    for url in args:
        if (not url.endswith(tuple(supported_extensions))):
            return False
    return True


def check_args(args):
    if len(args) <= 1:
        print("Usage: python3 ./scorpion FILE1 [FILE2 ...]")
        exit(1)
    if (check_ext(args[1:]) == False):
        print("Incorrect image extensions, supported image format are", supported_extensions)
        exit(1)

def exec():
    check_args(sys.argv)
    scorpion = Scorpion(sys.argv[1:])
    scorpion.launch()
    return ;

if __name__ == '__main__':
    exec()