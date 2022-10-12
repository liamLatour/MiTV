import itertools
import imghdr
from os import listdir
from os.path import isdir, isfile, join, abspath
import pickle
import multiprocessing

class Images():
   def __init__(self):      
        pass

   def run(self, paths):
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
            _path = self.sanitize(join(path, f))
            
            if isfile(_path) and imghdr.what(_path) == "jpeg":
                imgs_paths.append(abspath(_path))
            elif isdir(_path):
                self.parse_imgs(_path)

        res = pool.starmap(self.treat_img, zip(imgs_paths, itertools.repeat(data)))

        # Decompress received data
        data = self.decompress_data(data, res)

        if data != {}:
            with open(meta_path, 'wb') as f:
                pickle.dump(data, f)
   
   def sanitize(self, path):
        return path.replace('/', '\\')