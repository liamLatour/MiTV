from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
import time
import pickle

from os.path import isfile, join

class GetMetadata():
    def __init__(self, path):
        self.meta_path = join(path, ".people")
        self.get_metadata()
        
        event_handler = PatternMatchingEventHandler(["*"], None, False, True)
        event_handler.on_modified = self.get_metadata
        
        observer = Observer()
        observer.schedule(event_handler, self.meta_path, recursive=False)
        observer.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            observer.join()
        
    def get_metadata(self):
        if isfile(self.meta_path):
            with open(self.meta_path, 'rb') as f:
                self.data = pickle.load(f)
        else:
            self.data = None
        with open(self.meta_path, 'rb') as f:
            self.data = pickle.load(f)