import time
t1 = time.time()

import imghdr
from os import listdir
from os.path import isdir, isfile, join
import pickle
import face_recognition
import numpy as np
from img_similarity import ImageSimilarity


#TODO: Only treats jpeg for now
#TODO: reduce img size to accelerate process (maybe)
#TODO: Enable multiple pics for one person

refs = "C:\\Users\\liaml\\Projets\\ROOTS Template\\mi_tv_backend\\people_ref"
to_test = "C:\\Users\\liaml\\Projets\\ROOTS Template\\mi_tv_backend\\photos"
encoding_version = 1

#FIXME: Write on files at the end of sequence
# Cant do similarity in parallel unless I parallelize folders

class Images():
   def __init__(self, paths, sim=None):   
      self.sim = sim
      #self.pool = multiprocessing.Pool()
      for path in paths:
         self.parse_imgs(path)
   
   def parse_imgs(self, path):
      if isfile(path) and imghdr.what(path) == "jpeg":
         self.treat_img(self.sanitize(path))
      elif isdir(path):
         for f in listdir(path):
            self.parse_imgs(join(path, f))
   
   def sanitize(self, path):
      return path.replace('/', '\\')
   
   def treat_img(self, path):
      meta_path = join('\\'.join(path.split('\\')[0:-1]), ".people")
      data = {}
      
      if isfile(meta_path):
         with open(meta_path, 'rb') as f:
            data = pickle.load(f)

      if path not in data or "encoding_version" not in data[path] or data[path]["encoding_version"] != encoding_version:
         # higher num_jitters means higher resolution; model is large or small
         face_encoding = face_recognition.face_encodings(face_recognition.load_image_file(path), num_jitters=4, model="large")
         
         # Allows to already have data and not rewrite it (id or name for ref pics for example)
         if path in data:
            data[path]["encoding"] = face_encoding
            data[path]["encoding_version"] = encoding_version
         else:
            data[path] = {"encoding": face_encoding, "encoding_version": encoding_version}

      if len(data[path]["encoding"]) != 0: # otherwise no face has been seen TODO: tell user if it is a ref pic
         data = self.after_treatment(data, path)
         print(len(data[path]["encoding"]), "faces in", path)
      else:
         print("No faces in:", path)
         
      self.update_meta_data(data, path)
   
   def update_meta_data(self, data, path):
      meta_path = join('\\'.join(path.split('\\')[0:-1]), ".people")
      
      with open(meta_path, 'wb') as f:     
            pickle.dump(data, f)

class References(Images):
   def __init__(self, paths) -> None:
      self.face_paths = []
      self.face_encodings = []
      self.cur_id = 0
      super().__init__(paths)
   
   def after_treatment(self, data, path):
      self.face_encodings.append(data[path]["encoding"][0])
      self.face_paths.append(path)
      
      # Temp, only to give ids
      data[path]["id"] = self.cur_id
      self.cur_id += 1
      return data

class Photos(Images):
   def __init__(self, paths, references) -> None:
      self.ref = references
      
      # Used to mark similar pics
      self.sim = ImageSimilarity()
      self.last_pic = None
      self.group_nb = 0
      self.stopped = True
      
      self.check_similarity = False
      
      super().__init__(paths, sim=self.sim)
   
   def same_dir(self, path1, path2):
      return '\\'.join(path1.split('\\')[0:-1]) == '\\'.join(path2.split('\\')[0:-1])

   def after_treatment(self, data, path):
      ## Image similarity
      if self.check_similarity:
         if self.last_pic != None and self.same_dir(path, self.last_pic) and self.sim.is_similar(path, self.last_pic):
            if self.stopped:
               self.group_nb += 1
               data[path]["group_nb"] = self.group_nb
            data[self.last_pic]["group_nb"] = self.group_nb
            self.stopped = False
         else:
            self.stopped = True
         
         self.last_pic = path
      
      ## Facial recognition
      face_paths = []
      face_closeness = []
      
      if "faces" not in data[path]:
         data[path]["faces"] = ["?" for _ in range(len(data[path]["encoding"]))]
      
      old_names = data[path]["faces"]
      
      #TODO: is refactorable in a single for loop
      for face in data[path]["encoding"]:
         face_path = "?"

         face_distances = face_recognition.face_distance(self.ref.face_encodings, np.array(face))
         best_match_index = np.argmin(face_distances)
         if face_distances[best_match_index] < 0.6:
            face_path = self.ref.face_paths[best_match_index]

         face_paths.append(face_path)
         face_closeness.append(face_distances[best_match_index])

      for i in range(len(face_paths)):
         if face_paths[i] != old_names[i]:
            self.update_ref(path, old_names[i], face_paths[i], face_closeness[i])
            data[path]["faces"][i] = face_paths[i]

      return data

   def update_ref(self, path, old_face_path, face_path, closeness):
      ## Two way binding
      if face_path != '?':
         ref_meta_path = join('\\'.join(face_path.split('\\')[0:-1]), ".people")
      else:
         ref_meta_path = join('\\'.join(old_face_path.split('\\')[0:-1]), ".people")
      
      with open(ref_meta_path, 'rb') as f:
         ref_data = pickle.load(f)
      
      # Write it on ref
      if face_path != '?':
         if "seen_in" not in ref_data[face_path]:
            ref_data[face_path]["seen_in"] = {}
         
         ref_data[face_path]["seen_in"][path] = {
            "closeness": closeness
         }
      
      # Remove it from ref
      if old_face_path in ref_data and "seen_in" in ref_data[old_face_path] and path in ref_data[old_face_path]["seen_in"]:
         del ref_data[old_face_path]["seen_in"][path]
      
      with open(ref_meta_path, 'wb') as f:
         pickle.dump(ref_data, f)

if __name__ == '__main__':
   print(time.time() - t1)
   t = time.time()

   ref = References([refs])
   sample = Photos([to_test], ref)

   print(time.time() - t)