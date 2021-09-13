from tempfile import NamedTemporaryFile
import os


class TempImage(object):
    def __init__(self):
        self.file_obj = NamedTemporaryFile(suffix=".png", delete=False)
        self.file_obj.close()

    def __enter__(self):
        return self.file_obj

    def __exit__(self, type, value, traceback):
        os.unlink(self.file_obj.name)
