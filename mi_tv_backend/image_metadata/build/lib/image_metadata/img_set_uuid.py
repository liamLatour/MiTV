from os.path import isfile
import pickle

def add_uuid(uuid, img, meta_path):
    if isfile(meta_path):
        with open(meta_path, 'rb') as f:
            data = pickle.load(f)
    else:
        data = {}
        
    if img not in data:
        data[img] = {}
        
    data[img]["uuid"] = uuid
        
    with open(meta_path, 'wb') as f:
        pickle.dump(data, f)