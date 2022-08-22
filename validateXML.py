import os
import sys
import re
from lxml import etree

CHANGED_FILES = os.environ.get("CHANGED_FILES")

def validate(xml_path: str, xsd_path: str) -> bool:

    xmlschema_doc = etree.parse(xsd_path)
    xmlschema = etree.XMLSchema(xmlschema_doc)

    xml_doc = etree.parse(xml_path)
    result = xmlschema.validate(xml_doc)

    return result


rootdir = CHANGED_FILES.split()[0].split('/')[0]
print("rootdir:" + rootdir)
#Durchlaueft das gesamte Repo und checkt alle .xml Dateien

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        filepath = subdir + os.sep + file
        if filepath.endswith('.xml'):
            if validate(filepath, "./schema.xsd"):
                print(filepath + " valid!")
            else:
                print(filepath + " not vaild!")
                sys.exit(1)

sys.exit(0)
