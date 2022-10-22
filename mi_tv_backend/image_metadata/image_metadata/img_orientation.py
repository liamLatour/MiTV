from PIL import Image, ImageOps
from .parallel_images import Images
from . import db_interface
import click

class ImageOrientation(Images):
    def __init__(self):
        super().__init__()
    
    def treat_img(self, path):
        click.echo(path)
        
        image = ImageOps.exif_transpose(Image.open(path))
        db_interface.add_orientation_ai_meta(path, image.size[1] > image.size[0])
