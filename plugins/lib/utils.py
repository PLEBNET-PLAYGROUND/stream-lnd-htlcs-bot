#                  __       __   __
#   _______  __ __/ /____ _/ /  / /__   ___ ___  ___ ________
#  / __/ _ \/ // / __/ _ `/ _ \/ / -_) (_-</ _ \/ _ `/ __/ -_)
# /_/  \___/\_,_/\__/\_,_/_.__/_/\__(_)___/ .__/\_,_/\__/\__/
#                                        /_/
# We route payments.
# Provided as is. Use at own risk of being awesome.
#

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
