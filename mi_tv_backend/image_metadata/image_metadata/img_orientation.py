from PIL import Image, ImageOps
from os.path import isfile, join, abspath
import pickle
from .parallel_images import Images
import click

class ImageOrientation(Images):
    def __init__(self):
        super().__init__()
    
    def treat_img(self, path, data):
        click.echo(path)
        updates = {}
        image = None
        
        if path not in data or "is_portrait" not in data[path]:
            image = Image.open(path)
            image = ImageOps.exif_transpose(image)
            updates["is_portrait"] = image.size[1] > image.size[0]
        
        if path not in data or "date" not in data[path]:
            if image == None:
                image = Image.open(path)
            updates["date"] = image._getexif()[36867]
        
        return (path, updates)
    
    def decompress_data(self, data, res):
        for img in res:
            if img[0] not in data:
                data[img[0]] = {}
            
            for key in img[1]:
                data[img[0]][key] = img[1][key]
        return data

class GetOrientation():
    def __init__(self, path):
        meta_path = join(path, ".people")

        if isfile(meta_path):
            with open(meta_path, 'rb') as f:
                self.data = pickle.load(f)
        else:
            self.data = None
    
    def is_portrait(self, img_path):
        if self.data == None:
            return False
        
        img_data = self.data[abspath(img_path)]
        
        if "is_portrait" not in img_data:
            return False
        
        return img_data["is_portrait"]
