import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['AUTOGRAPH_VERBOSITY'] = '0'

import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
import numpy as np
from scipy.spatial import distance
from os.path import join
from os import listdir
import imghdr

tf.get_logger().setLevel('FATAL')
tf.autograph.set_verbosity(0)

##
#   CAREFUl: This assumes similar photos are in order
##

# https://towardsdatascience.com/image-similarity-with-deep-learning-c17d83068f59

class ImageSimilarity():
    def __init__(self) -> None:
        model_url = "https://tfhub.dev/tensorflow/efficientnet/lite0/feature-vector/2"

        self.IMAGE_SHAPE = (224, 224)

        self.layer = hub.KerasLayer(model_url, input_shape=self.IMAGE_SHAPE+(3,))
        self.model = tf.keras.Sequential([self.layer])

        self.metric = 'cosine'

    def extract(self, path):
        path = Image.open(path).convert('L').resize(self.IMAGE_SHAPE)
        path = np.stack((path,)*3, axis=-1)
        path = np.array(path)/255.0

        embedding = self.model.predict(path[np.newaxis, ...], verbose='0')
        vgg16_feature_np = np.array(embedding)
        flattended_feature = vgg16_feature_np.flatten()

        return flattended_feature

    def is_similar(self, path1, path2):
        return distance.cdist([self.extract(path1)], [self.extract(path2)], self.metric)[0]<.15

    # Only for debug purpose
    def mark_similar(self, path):
        # <.15 is good measure
        last_img = ""
        stoped = True
        
        for f in listdir(path):
            if imghdr.what(join(path, f)) != "jpeg":
                continue
            if last_img == "":
                last_img = join(path, f)
                continue
            cur_img = join(path, f)
            
            sim = self.img_similiraty(last_img, cur_img)
            if sim:
                if stoped:
                    print("###")
                    print(last_img)
                print(cur_img)
                stoped = False
            else:
                stoped = True
            last_img = cur_img
            
#mark_similar("C:\\Users\\liaml\\Projets\\ROOTS Template\\mi_tv_backend\\photos\\photo_desinté")