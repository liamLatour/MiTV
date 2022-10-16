from os.path import isfile, dirname, isdir
import threading
import time

import click
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from image_metadata import (ImageOrientation, ImageSimilarity, Photos,
                            References, ImageFormatHandler)

# run with:
#   meta_data_creation --continuous --immediate ./people_ref ./photos

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
        self.image_root_paths = image_root_paths
        self.continuous = continuous
        self.nightly = nightly
        self.prerun = prerun
        
        self.to_compute = []
        self.scheluded_ref_update = False
        
        self.orientation = ImageOrientation()
        self.similarity = ImageSimilarity()
        self.references = References(self.ref_path)
        self.face_recognition = Photos(self.references)
        self.format = ImageFormatHandler()
        
    def run(self):
        self.references.run()
        
        if not self.continuous or self.prerun:
            self.create_metadata()
        
        if self.continuous:
            # event handler
            event_handler = PatternMatchingEventHandler(["*"], None, False, True)
            event_handler.on_modified = self.event_handler
            event_handler.on_created  = self.event_handler
            event_handler.on_moved    = self.event_handler
            
            # observer
            observer = Observer()
            for path in self.image_root_paths:
                click.echo("Looking at: "+str(path))
                observer.schedule(event_handler, path, recursive=True)
            observer.start()
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
                observer.join()
                
            # ref event handler
            ref_event_handler = PatternMatchingEventHandler(["*"], None, False, True)
            ref_event_handler.on_modified = self.ref_event_handler
            ref_event_handler.on_created  = self.ref_event_handler
            ref_event_handler.on_moved    = self.ref_event_handler
            
            # ref observer
            ref_observer = Observer()
            ref_observer.schedule(ref_event_handler, self.ref_path, recursive=True)
            ref_observer.start()
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                ref_observer.stop()
                ref_observer.join()

    def event_handler(self, event):
        path = event.src_path
        
        if isfile(path):
            path = dirname(path)
        elif not isdir(path):
            click.echo(path + " is not dir or file")
            return
        
        if path not in self.to_compute:
            click.echo(path)
            
            self.to_compute.append(path)
        
            if self.nightly:
                # 24 h = 86400 sec
                cur_time = int(time.time())
                delay = cur_time - cur_time%86400 + 86400 # midnight gmt
            else:
                delay = 360 # 5 mins

            threading.Timer(delay, lambda: self.create_metadata(self.to_compute) ).start()
    
    def create_metadata(self, image_paths=None):
        if image_paths == None:
            image_paths = self.image_root_paths
        else:
            self.to_compute.remove(image_paths)
        
        click.echo("Started on paths:" + str(image_paths))
        
        t = time.time()
        click.echo("Orientation")
        self.orientation.run(image_paths)
        click.echo("Orientation finished in: " + str(time.time()-t))
        
        t1 = time.time()
        click.echo("Similarity")
        self.similarity.run(image_paths)
        click.echo("Similarity finished in: " + str(time.time()-t1))
        
        t1 = time.time()
        click.echo("Face recognition")
        self.face_recognition.run(image_paths)
        click.echo("Face recognition finished in: " + str(time.time()-t1))
        
        click.echo("Finished in: " + str(time.time()-t))
        
    def ref_event_handler(self, event):
        if self.scheluded_ref_update:
            return
        
        if self.nightly:
            # 24 h = 86400 sec
            cur_time = int(time.time())
            delay = cur_time - cur_time%86400 + 86400 # midnight gmt
        else:
            delay = 360 # 5 mins

        self.scheluded_ref_update = True
        threading.Timer(delay, self.create_ref_metadata).start()
    
    def create_ref_metadata(self):
        click.echo("Started on references")
        self.scheluded_ref_update = False
        
        t = time.time()
        click.echo("Reference face recognition")
        self.references.run()
        click.echo("Reference face recognition finished in: " + str(time.time()-t))
