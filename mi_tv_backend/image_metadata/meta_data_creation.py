from os.path import isfile, dirname, isdir, realpath, basename, relpath, join
from os import listdir
import threading
import time

import click
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from image_metadata import (ImageOrientation, ImageSimilarity, Photos,
                            References, ImageFormatHandler, Videos, db_interface)

# run with:
#   meta_data_creation --continuous --immediate ./people_ref ./photos
#   meta_data_creation --once --immediate ./people_ref ./photos

@click.command()
@click.argument("ref_path", type=click.Path(exists=True))
@click.argument("images_path", type=click.Path(exists=True), nargs=-1)
@click.option(
    "--continuous/--once",
    default=False,
    show_default=True
)
@click.option(
    "--nightly/--immediate",
    default=True,
    show_default=True
)
@click.option(
    "--prerun/--no-prerun",
    default=False
)
def cli(continuous, nightly, prerun, ref_path, images_path):
    """Script to generate image metadata"""    
    if images_path == None:
        click.echo("No images to treat")
        return
    
    click.echo("Runing with options:")
    click.echo("Nightly: "+str(nightly))
    click.echo("Continuous: "+str(continuous))
    click.echo("Images Paths: "+str(images_path))
    click.echo("References Paths: "+str(ref_path))
    
    meta_creation = MetadataCreation(ref_path, images_path, continuous, nightly, prerun)
    meta_creation.run()
    
class MetadataCreation():
    def __init__(self, ref_path, image_root_paths, continuous, nightly, prerun):
        self.ref_path = ref_path
        self.image_root_paths = []
        for path in image_root_paths:
            self.image_root_paths.append(realpath(path))
        self.continuous = continuous
        self.nightly = nightly
        self.prerun = prerun
        
        self.to_compute = []
        self.scheluded_ref_update = False
        self.delay = 10 # in secs
        
        self.orientation = ImageOrientation()
        self.similarity = ImageSimilarity()
        self.references = References(self.ref_path)
        self.face_recognition = Photos(self.references)
        self.format = ImageFormatHandler()
        self.vid = Videos()
        
    def run(self):
        # First run to initialize references
        self.references.run()
        
        if not self.continuous or self.prerun:
            self.create_metadata()
        
        if self.continuous:
            # event handler
            event_handler = FileSystemEventHandler()        # ["*"], None, False, True
            event_handler.on_created  = self.event_handler
            event_handler.on_deleted  = self.event_handler
            event_handler.on_moved    = self.event_handler
            
            # observer
            observer = Observer()
            for path in self.image_root_paths:
                click.echo("Looking at: "+str(path))
                observer.schedule(event_handler, realpath(path), recursive=True)
            observer.start()
                
            # ref event handler
            ref_event_handler = FileSystemEventHandler()        # ["*"], None, False, True
            ref_event_handler.on_modified = self.ref_event_handler
            ref_event_handler.on_created  = self.ref_event_handler
            ref_event_handler.on_moved    = self.ref_event_handler
            ref_event_handler.on_deleted  = self.ref_event_handler
            
            # ref observer
            ref_observer = Observer()
            ref_observer.schedule(ref_event_handler, realpath(self.ref_path), recursive=True)
            ref_observer.start()
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
                observer.join()
                ref_observer.stop()
                ref_observer.join()

    def actual_path(self, path):
        abs_beg_path = realpath(self.image_root_paths[0])
        path = realpath(path)
        path = relpath(path, abs_beg_path)

        if (path == '.'):
            path = ""

        return join(abs_beg_path.split("/")[-1], path)

    def event_handler(self, event):
        path = event.src_path

        match event.event_type:
            case "created":
                if isfile(path):
                    path = dirname(path)
                elif isdir(path):
                    db_interface.update_folder_representation(dirname(self.actual_path(path)))
                    db_interface.update_folder_representation(self.actual_path(path))
                else:
                    click.echo(path + " is not dir or file")
                    return
                
                if self.actual_path(path) not in self.to_compute:
                    if isdir(path) and self.vid.small_dir_name in basename(path):
                        return
                    
                    self.to_compute.append(self.actual_path(path))
                
                    if self.nightly:
                        # 24 h = 86400 sec
                        cur_time = int(time.time())
                        delay = cur_time - cur_time % 86400 + 86400 # midnight gmt
                    else:
                        delay = self.delay

                    threading.Timer(delay, lambda: self.create_metadata(self.to_compute)).start()

            case "moved":
                npath = event.dest_path

                if isfile(path):
                    path, npath = dirname(path), dirname(npath)
                    db_interface.update_folder_representation(self.actual_path(path))
                    db_interface.update_folder_representation(self.actual_path(npath))
                    db_interface.rename_file(self.actual_path(path), self.actual_path(npath))
                elif isdir(path):
                    db_interface.rename_folder(self.actual_path(path), self.actual_path(npath))

            case "deleted":
                if isfile(path):
                    path = dirname(path)
                    db_interface.update_folder_representation(self.actual_path(path))
                    db_interface.remove_file(self.actual_path(path))
                elif isdir(path):
                    db_interface.remove_folder(self.actual_path(path))
    
    def create_metadata(self, image_paths=None, full=True):
        if image_paths == None:
            image_paths = []
            for path in self.image_root_paths:
                image_paths.append(realpath(path))
                for npath in listdir(path):
                    if isdir(npath):
                        db_interface.update_folders_hash(npath)

        t = time.time()
        
        click.echo("Started on paths:" + str(image_paths))
        
        tmp = []
        for path in image_paths:
            tmp.append(self.actual_path(path))

        if full:               
            t1 = time.time()
            click.echo("Format")
            self.format.run(image_paths)
            click.echo("Format finished in: " + str(time.time()-t1))
        
            t1 = time.time()
            click.echo("Orientation")
            self.orientation.run(tmp)
            click.echo("Orientation finished in: " + str(time.time()-t1))

            t1 = time.time()
            click.echo("Similarity")
            self.similarity.run(tmp)
            click.echo("Similarity finished in: " + str(time.time()-t1))
            
            t1 = time.time()
            click.echo("Video handling")
            self.vid.run(image_paths)
            click.echo("Videos finished in: " + str(time.time()-t1))
            
            db_interface.update_folders_hash(tmp)
        
        t1 = time.time()
        click.echo("Face recognition")
        #self.face_recognition.run(tmp)
        click.echo("Face recognition finished in: " + str(time.time()-t1))

        click.echo("Finished in: " + str(time.time()-t))
        
        for path in image_paths:
            if path in self.to_compute:
                self.to_compute.remove(path)
        
    def ref_event_handler(self, event):
        if self.scheluded_ref_update:
            return
        
        if self.nightly:
            # 24 h = 86400 sec
            cur_time = int(time.time())
            delay = cur_time - cur_time%86400 + 86400 # midnight gmt
        else:
            delay = self.delay

        self.scheluded_ref_update = True
        threading.Timer(delay, self.create_ref_metadata).start()
    
    def create_ref_metadata(self, recheck_images=False):
        click.echo("Started on references")
        
        t = time.time()
        click.echo("Reference face recognition")
        self.references.run()
        click.echo("Reference face recognition finished in: " + str(time.time()-t))
        self.scheluded_ref_update = False
        
        if recheck_images:
            self.create_metadata(None, False)