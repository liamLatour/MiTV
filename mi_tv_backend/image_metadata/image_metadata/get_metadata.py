from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
import pickle
import json
from os.path import isfile, join

class GetMetadata():
    def __init__(self, path):
        self.meta_path = join(path, ".people")
        self.get_metadata()
        
        event_handler = PatternMatchingEventHandler(["*"], None, False, True)
        event_handler.on_modified = self.get_metadata
        event_handler.on_created = self.get_metadata
        event_handler.on_moved = self.get_metadata
        
        observer = Observer()
        observer.schedule(event_handler, path, recursive=False)
        observer.start()
        
    def get_metadata(self, file=None):
        if isfile(self.meta_path):
            with open(self.meta_path, 'rb') as f:
                self.data = pickle.load(f)
        else:
            self.data = None

class UpdateMetadata():
    def __init__(self, path):
        self.meta_path = join(path, ".meta")
        
        if isfile(self.meta_path):
            with open(self.meta_path) as f:
                self.data = json.load(f)
        else:
            self.data = None

    def update_metadata(self, new_metadata):
        metadata = self.data
        print(metadata)
        for key in new_metadata:
            metadata[key] = new_metadata[key]
        
        with open(self.meta_path, 'w') as f:
            json.dump(metadata, f)