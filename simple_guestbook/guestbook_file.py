import threading


class GuestbookFile:
    def __init__(self):
        self.lock = threading.Lock()
        self.file = None

    def open(self, filename):
        if self.file is None:
            # Open the file for writing, appending to any existing data
            self.file = open(filename, mode='a')

    def close(self):
        if self.file is not None:
            self.file.close()
            self.file = None

    def __enter__(self):
        self.lock.acquire()
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        self.lock.release()
