import face_recognition
import numpy as np
import click
from os.path import isdir, isfile, join, abspath, basename
from os import listdir, cpu_count
from math import floor
import imghdr
import multiprocessing
from .parallel_images import Images
from . import db_interface
from .vid_handler import Videos

vids = Videos()

encoding_version = 1

class SubImages(Images):
   def parse_imgs(self, path):
        if vids.small_dir_name in basename(path):
            return

        if self.multiprocessing:
            context = multiprocessing
            if "forkserver" in multiprocessing.get_all_start_methods():
                context = multiprocessing.get_context("forkserver")
            pool = context.Pool(processes=floor(cpu_count() / 4)) # None is max number
            
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

# Only one folder
class References(SubImages):
   def __init__(self, path) -> None:
      super().__init__(ignore_change=True)
      
      self.path = path
      self.face_paths = []
      self.face_encodings = []
      
   def run(self, path=None):
      if path == None:
         super().run([self.path])
      else:
         super().run([path])
   
   def treat_img(self, path):
      click.echo(path)
      
      encoding = db_interface.get_ai_encoding(path)
      
      if encoding == None or encoding["encoding_version"] < encoding_version:
         # higher num_jitters means higher resolution; model is large or small
         face_encoding = face_recognition.face_encodings(face_recognition.load_image_file(path), num_jitters=4, model="large")
         db_interface.add_ai_encoding(path, encoding_version, face_encoding)
      else:
         face_encoding = encoding["encoding"]

      return (path, face_encoding)
   
   def decompress_data(self, res):
      for img in res:
         path = img[0]
         encoding = img[1]
         
         if len(encoding) > 0:
            self.face_encodings.append(encoding[0])
            self.face_paths.append(path)
      
class Photos(SubImages):
   def __init__(self, references) -> None:
      super().__init__()
      self.ref = references
         
   def treat_img(self, path):
      click.echo(path)
            
      encoding = db_interface.get_ai_encoding(path)
      
      if encoding == None or encoding["encoding_version"] < encoding_version:
         # higher num_jitters means higher resolution; model is large or small
         face_encoding = face_recognition.face_encodings(face_recognition.load_image_file(path), num_jitters=4, model="large")
         db_interface.add_ai_encoding(path, encoding_version, face_encoding)
      else:
         face_encoding = encoding["encoding"]
      
      if len(face_encoding) > 0:
         self.after_treatment(face_encoding, path)

   def after_treatment(self, face_encoding, path):
      i = 0
      
      meta = db_interface.get_ai_meta(path)
      
      if meta == None or "faces" not in meta:
         old_names = ["?" for _ in range(len(face_encoding))]
         db_interface.add_ai_meta(path, old_names)
      else:
         old_names = meta["faces"]
         
      new_names = old_names
      
      for face in face_encoding:
         face_path = "?"

         face_distances = face_recognition.face_distance(self.ref.face_encodings, np.array(face))
         best_match_index = np.argmin(face_distances)
         if face_distances[best_match_index] < 0.6:
            face_path = self.ref.face_paths[best_match_index]

         if face_path != old_names[i]:
            self.update_ref(path, old_names[i], face_path, face_distances[best_match_index])
      
         new_names[i] = db_interface.sanitize_path(face_path)
         
         i += 1
      
      db_interface.add_ai_meta(path, new_names)

   def update_ref(self, path, old_face_path, face_path, closeness):
      # Write it on ref
      if face_path != '?':
         db_interface.add_reference_seen_in(face_path, path, closeness)
      
      # Remove it from ref
      db_interface.remove_reference_seen_in(old_face_path, path)
