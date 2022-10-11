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
        if self.data == None or abspath(img_path) not in self.data:
            return (True, None)
        
        img_data = self.data[abspath(img_path)]
        
        if "group_nb" not in img_data:
            return (True, None)
        
        if img_data["group_nb"] not in self.already_seen_groups:
            self.already_seen_groups.append(img_data["group_nb"])
            return (True, self.get_all_in_group(img_data["group_nb"]))
        
        return (False, None)
    
    def get_all_in_group(self, group_nb):
        list_paths = []
        
        for key in self.data:
            if "group_nb" in self.data[key] and self.data[key]["group_nb"]==group_nb:
                list_paths.append(key)
                
        return list_paths