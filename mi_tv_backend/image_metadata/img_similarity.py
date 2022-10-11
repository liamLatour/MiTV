import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['AUTOGRAPH_VERBOSITY'] = '0'

import imghdr
import pickle
import time
from os import listdir
from os.path import isdir, isfile, join, abspath

import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
from scipy.spatial import distance

tf.get_logger().setLevel('FATAL')
tf.autograph.set_verbosity(0)

to_test = "C:\\Users\\liaml\\Projets\\ROOTS Template\\mi_tv_backend\\photos"

##
#   CAREFUl: This assumes similar photos are in order
##

# https://towardsdatascience.com/image-similarity-with-deep-learning-c17d83068f59

# TODO: could parallelize folders
class ImageSimilarity():
    def __init__(self, paths):
        model_url = "https://tfhub.dev/tensorflow/efficientnet/lite0/feature-vector/2"

        self.IMAGE_SHAPE = (224, 224)

        self.layer = hub.KerasLayer(model_url, input_shape=self.IMAGE_SHAPE+(3,))
        self.model = tf.keras.Sequential([self.layer])

        self.metric = 'cosine'
        self.tolerance = 0.15
        
        self.paths = paths
        
    def run(self):
        for path in self.paths:
            assert isdir(path)
            self.parse_imgs(path)
            
    def parse_imgs(self, path):
        meta_path = join(path, ".people")
        data = {}

        if isfile(meta_path):
            with open(meta_path, 'rb') as f:
                data = pickle.load(f)
                
        last_pic = None
        last_pic_encoding = None
        group_nb = 0
        stopped = True
        
        for f in listdir(path):
            _path = self.sanitize(join(path, f))
            
            if isfile(_path) and imghdr.what(_path) == "jpeg":
                current_encoding = self.extract(_path)
                print(_path)
                
                if last_pic != None and distance.cdist([current_encoding], [last_pic_encoding], self.metric)[0] < self.tolerance:
                    if stopped:
                        group_nb += 1
                        data[_path]["group_nb"] = group_nb
                    data[last_pic]["group_nb"] = group_nb
                    stopped = False
                else:
                    stopped = True
                
                last_pic = _path
                last_pic_encoding = current_encoding
            elif isdir(_path):
                self.parse_imgs(_path)

        if data != {}:
            with open(meta_path, 'wb') as f:
                pickle.dump(data, f)

    def sanitize(self, path):
        return path.replace('/', '\\')
    
    def extract(self, path):
        path = Image.open(path).convert('L').resize(self.IMAGE_SHAPE)
        path = np.stack((path,)*3, axis=-1)
        path = np.array(path)/255.0

        embedding = self.model.predict(path[np.newaxis, ...], verbose='0')
        vgg16_feature_np = np.array(embedding)
        flattended_feature = vgg16_feature_np.flatten()

        return flattended_feature

class GetGroups():
    def __init__(self, path):
        self.already_seen_groups = []
        self.groups = {}
        meta_path = join(path, ".people")

        if isfile(meta_path):
            with open(meta_path, 'rb') as f:
                self.data = pickle.load(f)
        else:
            self.data = None
            
    def get_groups(self):
        if self.data == None:
            return
            
        for key in self.data:
            if "group_nb" in self.data[key]:
                if self.data[key]["group_nb"] not in self.groups:
                    self.groups[self.data[key]["group_nb"]] = []    
                
                self.groups[self.data[key]["group_nb"]].append(key)
    
    def is_not_in_group(self, img_path):
        if self.data == None or abspath(img_path) not in self.data:
            return (True, None)
        
        img_data = self.data[abspath(img_path)]
        
        if "group_nb" not in img_data:
            return (True, None)
        
        if img_data["group_nb"] not in self.already_seen_groups:
            self.already_seen_groups.append(img_data["group_nb"])
            return (True, self.groups[img_data["group_nb"]])
        
        return (False, None)

if __name__ == '__main__':
    t = time.time()
    sim = ImageSimilarity([to_test])
    sim.run()
    print(time.time() - t)
