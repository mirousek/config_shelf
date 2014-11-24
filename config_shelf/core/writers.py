from lxml import etree
import re
import xml.dom.minidom

__author__ = 'miroslav.stepanek'

class BaseWriter(object):
    def write(self):
        pass

class FileWriter(BaseWriter):
    file = None

    def detect_line_endings(self):
        f = open(self.file.get_file_path(), mode='rU')

    def __init__(self, file):
        self.file = file

class XmlFileWriter(FileWriter):
    def __init__(self, file, xpath, attr=None, reformat=False):
        super(XmlFileWriter, self).__init__(file)
        self.xpath = xpath
        self.attr = attr
        self.reformat = reformat

    def write(self, value):
        self.detect_line_endings()
        tree = etree.parse(self.file.get_file_path())
        root = tree.getroot()

        nodes = tree.xpath(self.xpath)
        if len(nodes) == 0:
            raise RuntimeError("Node '{0}' not found in {1}".format(self.xpath, self.file.get_file_path()))
        if len(nodes) > 1:
            raise RuntimeError("Node '{0}' in {1} found multiple times ({3}x)".format(self.xpath, self.file.get_file_path()), len(nodes))

        node = nodes[0]
        if self.attr:
            node.set(self.attr, value)
        else:
            node.text = value

        s = etree.tostring(tree, xml_declaration=True, pretty_print=True, encoding="utf-8")

        # s = s.replace('\r\n', '\n').replace('\n', '\r\n')
        # s = '\r'
        # s = s.replace('\n', 'Q')
        # s = re.sub(r'<([^>]*[^> ])/>', r'<\1 />', s)
        if self.reformat:
            pretty_print = lambda xmlstring: '\n'.join([line for line in xml.dom.minidom.parseString(xmlstring).toprettyxml(indent=' '*4, encoding="utf-8").split('\n') if line.strip()])
            s = pretty_print(s)

        # x = xml.dom.minidom.parseString(s)
        # s = x.toprettyxml()
        s = re.sub(r'<([^>]*[^> ])/>', r'<\1 />', s)
        f = open(self.file.get_file_path(), "w")
        f.write(s)
        f.close()
        # tree.write(self.file.get_file_path(), xml_declaration=True)
