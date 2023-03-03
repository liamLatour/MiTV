import imghdr
from os import listdir
from os.path import isdir, isfile, join, abspath, basename
import multiprocessing

from .vid_handler import Videos
from . import db_interface

vids = Videos()

class Images():
    def __init__(self, ignore_change=False) -> None:
        # Set to true to recompute even if no changes have been made to the folder
        self.ignore_change = ignore_change
        self.multiprocessing = True
    
    def run(self, paths):
        for path in paths:
            assert isdir(path)
            if self.ignore_change or db_interface.folder_changed(path):
                self.parse_imgs(path)
    
    def parse_imgs(self, path):
        if vids.small_dir_name in basename(path):
            return

        if self.multiprocessing:
            context = multiprocessing
            if "forkserver" in multiprocessing.get_all_start_methods():
                context = multiprocessing.get_context("forkserver")
            pool = context.Pool(processes=None) # None is max number
            
        imgs_paths = []
        
        for f in listdir(path):
            _path = abspath(db_interface.sanitize_path(join(path, f)))
            
            if isfile(_path) and imghdr.what(_path) == "jpeg":
                imgs_paths.append(_path)
            elif isdir(_path):
                self.parse_imgs(_path)

        if self.multiprocessing:
            res = pool.starmap(self.treat_img, zip(imgs_paths))
        else:
            res = []
            for path in imgs_paths:
                res.append(self.treat_img(path))

        # Decompress received data
        self.decompress_data(res)
   
    def sanitize(self, path):
        return abspath(path.replace('/', '\\'))
    
    def decompress_data(self, res):
        return