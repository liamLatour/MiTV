import itertools
import time
t1 = time.time()

import imghdr
from os import listdir
from os.path import isdir, isfile, join
import pickle
import face_recognition
import numpy as np
import multiprocessing
from .parallel_images import Images


refs = "C:\\Users\\liaml\\Projets\\ROOTS Template\\mi_tv_backend\\people_ref"
to_test = "C:\\Users\\liaml\\Projets\\ROOTS Template\\mi_tv_backend\\photos"
encoding_version = 1

#FIXME: Write on files at the end of sequence

class Images_old():
   def __init__(self, paths):      
      self.paths = paths

   def run(self):
      for path in self.paths:
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
            imgs_paths.append(_path)
            #self.treat_img(_path)
         elif isdir(_path):
            self.parse_imgs(_path)

      res = pool.starmap(self.treat_img, zip(imgs_paths, itertools.repeat(data)))

      # Decompress received data
      data = self.decompress_data(data, res)

      if data != {}:
         with open(meta_path, 'wb') as f:
               pickle.dump(data, f)

      #if isfile(path) and imghdr.what(path) == "jpeg":
      #   self.treat_img(self.sanitize(path))
      #elif isdir(path):
      #   for f in listdir(path):
      #      self.parse_imgs(join(path, f))
   
   def sanitize(self, path):
      return path.replace('/', '\\')
   
   def treat_img(self, path, data):
      #meta_path = join('\\'.join(path.split('\\')[0:-1]), ".people")
      #data = {}
      #
      #if isfile(meta_path):
      #   with open(meta_path, 'rb') as f:
      #      data = pickle.load(f)
      updates = {}
      face_encoding = None

      if path not in data or "encoding_version" not in data[path] or data[path]["encoding_version"] != encoding_version:
         # higher num_jitters means higher resolution; model is large or small
         face_encoding = face_recognition.face_encodings(face_recognition.load_image_file(path), num_jitters=4, model="large")
         
         updates["encoding"] = face_encoding
         updates["encoding_version"] = encoding_version
         
         # Allows to already have data and not rewrite it (id or name for ref pics for example)
         #if path in data:
         #   data[path]["encoding"] = face_encoding
         #   data[path]["encoding_version"] = encoding_version
         #else:
         #   data[path] = {"encoding": face_encoding, "encoding_version": encoding_version}
      else:
         face_encoding = data["encoding"]

      if len(face_encoding) != 0: # otherwise no face has been seen TODO: tell user if it is a ref pic
         data = self.after_treatment(data, path)
         #print(len(data[path]["encoding"]), "faces in", path)
      else:
         print("No faces in:", path)
      
      return (path, updates)
         
      #self.update_meta_data(data, path)
   
   #def update_meta_data(self, data, path):
   #   meta_path = join('\\'.join(path.split('\\')[0:-1]), ".people")
   #   
   #   with open(meta_path, 'wb') as f:     
   #         pickle.dump(data, f)

# Only one folder
class References(Images):
   def __init__(self, path) -> None:
      super().__init__([path])
      
      self.face_paths = []
      self.face_encodings = []
      self.cur_id = 0
      self.metapath = join(path, ".people")
      
   def treat_img(self, path, data):
      print(path)
      updates = {}

      if path not in data or "encoding_version" not in data[path] or data[path]["encoding_version"] != encoding_version:
         # higher num_jitters means higher resolution; model is large or small
         face_encoding = face_recognition.face_encodings(face_recognition.load_image_file(path), num_jitters=4, model="large")
         
         updates["encoding"] = face_encoding
         updates["encoding_version"] = encoding_version

      return (path, updates)
   
   def decompress_data(self, data, res):
      for img in res:
         if  img[1] != {}:
            if img[0] not in data:
               data[img[0]] = {
                  "encoding": img[1]["encoding"],
                  "encoding_version": img[1]["encoding_version"]
               }
            else:
               data[img[0]]["encoding"] = img[1]["encoding"]
               data[img[0]]["encoding_version"] = img[1]["encoding_version"]
         
         if len(data[img[0]]["encoding"]) > 0: # FIXME: shouldn't have to put this
            self.face_encodings.append(data[img[0]]["encoding"][0])
            self.face_paths.append(img[0])
         
         # Temp, only to give ids
         data[img[0]]["id"] = self.cur_id
         self.cur_id += 1
      
      return data
      
class Photos(Images):
   def __init__(self, paths, references) -> None:
      super().__init__(paths)
      
      self.ref = references
         
   def treat_img(self, path, data):
      print(path)
      updates = {}

      if path not in data or "encoding_version" not in data[path] or data[path]["encoding_version"] != encoding_version:
         # higher num_jitters means higher resolution; model is large or small
         face_encoding = face_recognition.face_encodings(face_recognition.load_image_file(path), num_jitters=4, model="large")
         
         updates["encoding"] = face_encoding
         updates["encoding_version"] = encoding_version
      else:
         face_encoding = data[path]["encoding"]
      
      ref_updates = {}
      if len(face_encoding) > 0:
         updates, ref_updates = self.after_treatment(face_encoding, data, path, updates)
      
      return (path, updates, ref_updates)
    
   def decompress_data(self, data, res):
      with open(self.ref.metapath, 'rb') as f:
         ref_data = pickle.load(f)
      
      for img in res:
         if img[0] not in data:
            data[img[0]] = {}
            
         # Update data
         for key in img[1]:
            data[img[0]][key] = img[1][key]
            
         # Update ref data
         for key in img[2]:
            if "del" in img[2][key]:
               del ref_data[img[2][key]["del"]]["seen_in"][img[0]]
            if "seen_in" in img[2][key]:
               if "seen_in" not in ref_data[key]:
                  ref_data[key]["seen_in"] = {}
               
               ref_data[key]["seen_in"][img[0]] = {
                  "closeness": ref_data[key]["closeness"]
               }
         
      with open(self.ref.metapath, 'wb') as f:
         pickle.dump(ref_data, f)
      
      return data

   def after_treatment(self, face_encoding, data, path, updates):
      face_paths = []
      face_closeness = []
      
      if "faces" not in data[path]:
         updates["faces"] = ["?" for _ in range(len(face_encoding))]
         old_names = updates["faces"]
      else:
         old_names = data[path]["faces"]
      
      #TODO: is refactorable in a single for loop
      for face in face_encoding:
         face_path = "?"

         face_distances = face_recognition.face_distance(self.ref.face_encodings, np.array(face))
         best_match_index = np.argmin(face_distances)
         if face_distances[best_match_index] < 0.6:
            face_path = self.ref.face_paths[best_match_index]

         face_paths.append(face_path)
         face_closeness.append(face_distances[best_match_index])

      ref_updates = {}

      for i in range(len(face_paths)):
         if face_paths[i] != old_names[i]:
            ref_updates = self.update_ref(path, old_names[i], face_paths[i], face_closeness[i], ref_updates)
            updates["faces"][i] = face_paths[i]

      return (updates, ref_updates)

   def update_ref(self, path, old_face_path, face_path, closeness, ref_updates):
      # Write it on ref
      if face_path != '?':
         ref_updates[face_path] = {"seen_in": path, "closeness": closeness}
      
      # Remove it from ref
      if old_face_path in self.ref_data and "seen_in" in self.ref_data[old_face_path] and path in self.ref_data[old_face_path]["seen_in"]:
         ref_updates[face_path] = {"del": old_face_path}
      
      return ref_updates

if __name__ == '__main__':
   print(time.time() - t1)
   t = time.time()

   ref = References(refs)
   ref.run()
   sample = Photos([to_test], ref)
   sample.run()

   print(time.time() - t)