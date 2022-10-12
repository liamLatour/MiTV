from image_metadata import ImageSimilarity

#from img_similarity import ImageSimilarity
#from img_orientation import ImageOrientation
#from img_facial_recognition import References, Photos

import click


@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def test(name):
    print(name)

class MetadataCreation():
    def __init__(self, ref_path, image_root_paths):
        self.ref_path = ref_path
        self.image_root_paths = image_root_paths
        
        self.orientation = ImageOrientation(self.image_root_paths)
        self.similarity = ImageSimilarity(self.image_root_paths)
        self.references = References(self.ref_path)
        self.face_recognition = Photos(self.image_root_paths, self.references)

    def create_metadata(self):
        self.orientation.run()
        self.similarity.run()
        self.references.run()
        self.face_recognition.run()
        
if __name__ == '__main__':
    refs = "C:\\Users\\liaml\\Projets\\ROOTS Template\\mi_tv_backend\\people_ref"
    to_test = "C:\\Users\\liaml\\Projets\\ROOTS Template\\mi_tv_backend\\photos"
    meta_creation = MetadataCreation(refs, [to_test])