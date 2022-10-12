import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['AUTOGRAPH_VERBOSITY'] = '0'

import imghdr
import pickle
import time
from os import listdir
from os.path import isdir, isfile, join, abspath

import numpy as np
from PIL import Image
from scipy.spatial import distance
import click


to_test = "C:\\Users\\liaml\\Projets\\ROOTS Template\\mi_tv_backend\\photos"

##
#   CAREFUl: This assumes similar photos are in order
##

# https://towardsdatascience.com/image-similarity-with-deep-learning-c17d83068f59

#FIXME: Problem with duplicates in groups display

# TODO: could parallelize folders
class ImageSimilarity():
    def __init__(self):
        
        import tensorflow as tf
        import tensorflow_hub as hub
        
        tf.get_logger().setLevel('FATAL')
        tf.autograph.set_verbosity(0)
        
        model_url = "https://tfhub.dev/tensorflow/efficientnet/lite0/feature-vector/2"

        self.IMAGE_SHAPE = (224, 224)

        self.layer = hub.KerasLayer(model_url, input_shape=self.IMAGE_SHAPE+(3,))
        self.model = tf.keras.Sequential([self.layer])

        self.metric = 'cosine'
        self.tolerance = 0.15
        
    def run(self, paths):
        for path in paths:
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
        groups = {}
        
        for f in listdir(path):
            _path = abspath(self.sanitize(join(path, f)))
            
            if isfile(_path) and imghdr.what(_path) == "jpeg":
                current_encoding = self.extract(_path)
                click.echo(_path)
                
                if last_pic != None and distance.cdist([current_encoding], [last_pic_encoding], self.metric)[0] < self.tolerance:
                    if stopped:
                        group_nb += 1
                        data[_path]["group_nb"] = group_nb
                        groups[group_nb] = [_path]
                    data[last_pic]["group_nb"] = group_nb
                    groups[group_nb].append(last_pic)
                    stopped = False
                else:
                    stopped = True
                
                last_pic = _path
                last_pic_encoding = current_encoding
            elif isdir(_path):
                self.parse_imgs(_path)
        
        data["groups"] = groups

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
        meta_path = join(path, ".people")

        if isfile(meta_path):
            with open(meta_path, 'rb') as f:
                self.data = pickle.load(f)
        else:
            self.data = None
    
    def is_not_in_group(self, img_path):
        if self.data == None or abspath(img_path) not in self.data:
            return (True, None)
        
        img_data = self.data[abspath(img_path)]
        
        if "group_nb" not in img_data:
            return (True, None)
        
        if img_data["group_nb"] not in self.already_seen_groups:
            self.already_seen_groups.append(img_data["group_nb"])
            return (True, self.data["groups"][img_data["group_nb"]])
        
        return (False, None)

if __name__ == '__main__':
    t = time.time()
    sim = ImageSimilarity([to_test])
    sim.run()
    click.echo(time.time() - t)
