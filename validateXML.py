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


#Setz den rootdir auf den aktuellen Firmenordner
rootdir = CHANGED_FILES.split()[0].split('/')[0]

#Wenn keine Aenderungen erkannt werden, bzw. eine Aenderung 1:1 rueckgaengig gemacht wurde, 
#ist der Test gueltig
if CHANGED_FILES == "":
    print("No changes detected.")
    sys.exit(0)

#Checkt REGEX, ob Dateinamen gueltig sind
#Gueltig ist nur wenn: Nur kleine Buchstaben, nur Zahlen, nur Bindestriche, muss mit '.xml' enden
for file in CHANGED_FILES.split():
    if not re.match('^[a-z0-9-]*\.xml?$', file.split('/')[-1]):
        print("Invalid file name!")
        sys.exit(1)

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
