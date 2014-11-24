import os
from writers import XmlFileWriter

__author__ = 'miroslav.stepanek'

class ValueDefinition(object):
    targets = []
    def __init__(self, targets=None):
        if targets:
            self.targets = targets

    def add_target(self, target):
        self.targets.append(target)

class FileDefinition(object):
    def __init__(self, filename):
        self.filename = filename

    def get_file_path(self):
        return os.path.join(FileDefinition.base_path, self.filename)

class XmlFileDefinition(FileDefinition):
    def writer(self, xpath, attr=None, reformat=False):
        writer = XmlFileWriter(self, xpath, attr, reformat)
        return writer
