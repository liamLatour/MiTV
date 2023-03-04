import imghdr
from PIL import Image
from os.path import join, abspath, isfile, isdir, splitext, basename, dirname
from os import listdir, rename
from .parallel_images import Images
from .vid_handler import Videos
from . import db_interface
import click
import multiprocessing

vids = Videos()

class ImageFormatHandler(Images):
    def __init__(self):
        super().__init__()

    def parse_imgs(self, path):
        if vids.small_dir_name in basename(path):
            return

        context = multiprocessing
        if "forkserver" in multiprocessing.get_all_start_methods():
            context = multiprocessing.get_context("forkserver")
        pool = context.Pool(processes=None) # None is max number
        
        imgs_paths = []
        
        for f in listdir(path):
            _path = abspath(db_interface.sanitize_path(join(path, f)))
            
            if isfile(_path) and self.is_supported_format(_path) and (basename(_path)[0] != '.'):
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

        filename = basename(path)
        filename = '.' + filename
        dir = dirname(path)
        rename(path, join(dir, filename))

    def is_supported_format(self, path):
        supported_formats = ["bmp", "png", "webp", "tiff", "gif"]

        return (imghdr.what(path) in supported_formats)