from os.path import join
import pickle

class GetFaces():
    def __init__(self):
        ref_path = "C:\\Users\\liaml\\Projets\\ROOTS Template\\mi_tv_backend\\people_ref"
        meta_path = join(ref_path, ".people")
        
        with open(meta_path, 'rb') as f:
            self.data = pickle.load(f)
    
    # Should be the only one used, it allows multiple ref images
    def get_face_by_id(self, id, order_by_closeness=True):
        imgs_path = []
        
        for p in self.data:
            if self.data[p]["id"] == id:
                imgs_path.extend(list(self.data[p]["seen_in"].items()))
                
        if order_by_closeness:
            imgs_path.sort(key=lambda x:x[1]["closeness"])
        
        return imgs_path

    def get_face_by_name(self, name, order_by_closeness=True):
        imgs_path = []
    
        for p in self.data:
            if name in p and "seen_in" in self.data[p]:
                imgs_path.extend(list(self.data[p]["seen_in"].items()))

        if order_by_closeness:
            imgs_path.sort(key=lambda x:x[1]["closeness"])

        return imgs_path

if __name__ == '__main__':
    get_face = GetFaces()
    
    print(get_face.get_face_by_name("test"))