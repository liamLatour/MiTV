from PIL import Image, ImageOps
from .parallel_images import Images
from . import db_interface
import click
import os
import datetime

class ImageOrientation(Images):
    def __init__(self):
        super().__init__()
    
    def treat_img(self, path):
        click.echo(path)
        
        image = Image.open(path)
        image_trans = ImageOps.exif_transpose(image)  
        
        date = image.getexif().get(306)
        if date == None:
            date = os.path.getctime(path)
        else:
            date = datetime.datetime.strptime(date, "%Y:%m:%d %H:%M:%S").timestamp()
        
        db_interface.add_exif_ai_meta(
            path,
            image_trans.size[1] > image_trans.size[0],
            date)
