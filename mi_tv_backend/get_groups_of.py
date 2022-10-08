from os.path import join, abspath, isfile
import pickle

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
        if self.data == None:
            return True
        
        img_data = self.data[abspath(img_path)]
        
        if "group_nb" not in img_data:
            return True
        
        if img_data["group_nb"] not in self.already_seen_groups:
            self.already_seen_groups.append(img_data["group_nb"])
            return True
        
        return False