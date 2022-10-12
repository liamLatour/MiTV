from PIL import Image, ImageOps
from os.path import isfile, join, abspath
import pickle
import time
from .parallel_images import Images


to_test = "C:\\Users\\liaml\\Projets\\ROOTS Template\\mi_tv_backend\\photos"

class ImageOrientation(Images):
    def __init__(self, paths):
        super().__init__(paths)
    
    def treat_img(self, path, data):
        print(path)
        
        if "is_portrait" not in data[path]:
            image = Image.open(path)
            image = ImageOps.exif_transpose(image)
            is_portrait = image.size[1] > image.size[0]
        else:
            return (path, data[path]["is_portrait"])
        
        return (path, is_portrait)
    
    def decompress_data(self, data, res):
        for img in res:
            if img[0] not in data:
                data[img[0]] = {
                    "is_portrait": img[1]
                }
            else:
                data[img[0]]["is_portrait"] = img[1]
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

if __name__ == '__main__':
    t = time.time()
    orient = ImageOrientation([to_test])
    orient.run()
    print(time.time() - t)
