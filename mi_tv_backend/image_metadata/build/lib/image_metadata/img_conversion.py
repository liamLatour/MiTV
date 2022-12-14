import imghdr
from PIL import Image
from os.path import join, abspath, isfile, isdir, splitext, basename
from os import listdir
from .parallel_images import Images
from .vid_handler import Videos
import click
import multiprocessing

class ImageFormatHandler(Images):
    def __init__(self):
        super().__init__()

    def parse_imgs(self, path):
        if Videos.small_dir_name in basename(path):
            return

        context = multiprocessing
        if "forkserver" in multiprocessing.get_all_start_methods():
            context = multiprocessing.get_context("forkserver")
        pool = context.Pool(processes=None) # None is max number
        
        imgs_paths = []
        
        for f in listdir(path):
            _path = self.sanitize(join(path, f))
            
            if isfile(_path) and self.is_supported_format(_path):
                imgs_paths.append(abspath(_path))
            elif isdir(_path):
                self.parse_imgs(_path)

        pool.starmap(self.treat_img, zip(imgs_paths))

    def treat_img(self, path):
        click.echo("Converting " + path + " to jpeg format...")

        with Image.open(path) as image:
            if imghdr.what(path) == "gif":
                image.seek(0)
            
            image = image.convert("RGB")
            image.save(splitext(path)[0] + ".jpg")

    def is_supported_format(self, path):
        supported_formats = ["bmp", "png", "webp", "tiff", "gif"]

        return (imghdr.what(path) in supported_formats)