import imghdr
from PIL import Image, ImageOps
from os.path import basename, dirname, join, abspath, isfile, isdir, splitext
from os import listdir, remove
from .get_metadata import GetMetadata
from .parallel_images import Images
import click

class ImageFormatHandler(Images):
    def __init__(self):
        super().__init__()

    def is_supported_format(self, path):
        supported_formats = ["bmp", "png", "webp", "tiff", "gif"]

        return (imghdr.what(path) in supported_formats)

    def convert_to_jpeg(self, path):
        with Image.open(path) as image:
            if imghdr.what(path) == "gif":
                image.seek(0)
                
            image = image.convert("RGB")
            image.save(splitext(path)[0] + ".jpg")

    def parse_imgs(self, path):       
        for f in listdir(path):
            if not any(x in f for x in ["jpg", "jpeg"]):
                _path = abspath(self.sanitize(join(path, f)))

                if isfile(_path) and self.is_supported_format(_path):
                    click.echo("Converting " + f + " to jpeg format...")
                    self.convert_to_jpeg(_path)
                    remove(_path)

                elif isdir(_path):
                    self.parse_imgs(_path)