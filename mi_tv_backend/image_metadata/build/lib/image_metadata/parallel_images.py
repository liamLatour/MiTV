import imghdr
from os import listdir
from os.path import isdir, isfile, join, abspath, basename
import multiprocessing

from .vid_handler import Videos

class Images():
    def __init__(self):      
        pass

    def run(self, paths):
        for path in paths:
            assert isdir(path)
            self.parse_imgs(path)
    
    def parse_imgs(self, path):
        if Videos.small_dir_name in basename(path):
            return

        context = multiprocessing
        if "forkserver" in multiprocessing.get_all_start_methods():
            context = multiprocessing.get_context("forkserver")
        pool = context.Pool(processes=8) # None is max number
        
        imgs_paths = []
        
        for f in listdir(path):
            _path = self.sanitize(join(path, f))
            
            if isfile(_path) and imghdr.what(_path) == "jpeg":
                imgs_paths.append(_path)
            elif isdir(_path):
                self.parse_imgs(_path)

        res = pool.starmap(self.treat_img, zip(imgs_paths))

        # Decompress received data
        self.decompress_data(res)
   
    def sanitize(self, path):
        return abspath(path.replace('/', '\\'))
    
    def decompress_data(self, res):
        return