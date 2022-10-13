from image_metadata import ImageSimilarity, ImageOrientation, References, Photos
import click


@click.command()
def cli():
    """Example script."""
    click.echo('Hello World!')

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
    refs = "people_ref"
    to_test = "photos"
    meta_creation = MetadataCreation(refs, [to_test])