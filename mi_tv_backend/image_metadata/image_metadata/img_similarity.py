import os
import sys

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['AUTOGRAPH_VERBOSITY'] = '0'

import imghdr
from os import listdir
from os.path import isdir, isfile, join, abspath, basename

import numpy as np
from PIL import Image
from scipy.spatial import distance
import click
from .vid_handler import Videos
from . import db_interface

##
#   CAREFUl: This assumes similar photos are in order
##

# https://towardsdatascience.com/image-similarity-with-deep-learning-c17d83068f59

# TODO: could parallelize encoding, then sequential treatment
class ImageSimilarity():
    def __init__(self):
        import tensorflow as tf
        import tensorflow_hub as hub
        
        tf.get_logger().setLevel('FATAL')
        tf.autograph.set_verbosity(0)
        
        model_path = join(sys.prefix,"image_metadata/efficientnet_lite0_feature-vector_2")

        self.IMAGE_SHAPE = (224, 224)

        self.layer = hub.KerasLayer(model_path, input_shape=self.IMAGE_SHAPE+(3,))
        self.model = tf.keras.Sequential([self.layer])

        self.metric = 'cosine'
        self.tolerance = 0.2
        
        self.group_nb = 0
        
    def run(self, paths):
        for path in paths:
            assert isdir(path)
            if Videos.small_dir_name not in basename(path) and db_interface.folder_changed(path):
                self.parse_imgs(path)

    def parse_imgs(self, path):
        last_pic = None
        last_pic_encoding = None
        stopped = True
        
        display = []
        groups = []
        
        for f in listdir(path):
            _path = abspath(db_interface.sanitize_path(join(path, f)))
            
            if isfile(_path) and imghdr.what(_path) == "jpeg":
                click.echo(_path)
                current_encoding = self.extract(_path)
                
                if last_pic != None and distance.cdist([current_encoding], [last_pic_encoding], self.metric)[0] < self.tolerance:
                    if stopped:
                        db_interface.add_group_ai_meta(last_pic, self.group_nb, False)
                    db_interface.add_group_ai_meta(_path, self.group_nb)
                    stopped = False
                elif not stopped:
                    self.group_nb += 1
                    stopped = True
                
                last_pic = _path
                last_pic_encoding = current_encoding
            elif isdir(_path):
                self.parse_imgs(_path)
    
    def extract(self, path):
        path = Image.open(path).convert('L').resize(self.IMAGE_SHAPE)
        path = np.stack((path,)*3, axis=-1)
        path = np.array(path)/255.0

        embedding = self.model.predict(path[np.newaxis, ...], verbose='0')
        vgg16_feature_np = np.array(embedding)
        flattended_feature = vgg16_feature_np.flatten()

        return flattended_feature
