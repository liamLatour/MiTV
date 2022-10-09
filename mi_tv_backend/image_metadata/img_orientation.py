from PIL import Image, ImageOps
from os.path import isdir, isfile, join, abspath
from os import listdir
import imghdr
import pickle
import time
import multiprocessing

to_test = "C:\\Users\\liaml\\Projets\\ROOTS Template\\mi_tv_backend\\photos"

class ImageOrientation():
    def __init__(self, paths):
        for path in paths:
            assert isdir(path)
            self.parse_imgs(path)

    def parse_imgs(self, path):
        meta_path = join(path, ".people")
        data = {}

        context = multiprocessing
        if "forkserver" in multiprocessing.get_all_start_methods():
            context = multiprocessing.get_context("forkserver")
        pool = context.Pool(processes=None) # None is max number

        if isfile(meta_path):
            with open(meta_path, 'rb') as f:
                data = pickle.load(f)
        
        imgs_paths = []
        
        for f in listdir(path):
            _path = join(path, f)
            
            if isfile(_path) and imghdr.what(_path) == "jpeg":
                #self.treat_img(self.sanitize(_path))
                imgs_paths.append(_path)              
            elif isdir(_path):
                self.parse_imgs(_path)
                
        res = pool.map(self.treat_img, imgs_paths)

        # Decompress received data
        for img in res:            
            if img[0] not in data:
                data[img[0]] = {
                    "is_portrait": img[1]
                }
            else:
                data[img[0]]["is_portrait"] = img[1]

        if data != {}:
            with open(meta_path, 'wb') as f:
                pickle.dump(data, f)

    def sanitize(self, path):
        return path.replace('/', '\\')
    
    def treat_img(self, path):
        print(path)
        image = Image.open(path)
        image = ImageOps.exif_transpose(image)
        is_portrait = image.size[1] > image.size[0]
        
        return (path, is_portrait)

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
    print(time.time() - t)
