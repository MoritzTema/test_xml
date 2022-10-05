import os
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom

#List die productID aus
def getProductID(path):
    tree = ET.parse(path)
    root = tree.getroot()
    device = root.find('Device')
    productID = device.get('Product_ID')

    return(productID)


def createXML(paths, IDs):
    root = minidom.Document()
    xml = root.createElement('index')
    root.appendChild(xml)

    for id in range(len(IDs)):
        productChild = root.createElement('Product')

        productChild.setAttribute('Path', str(paths[id]))
        productChild.setAttribute('Product_ID', str(IDs[id]))
        xml.appendChild(productChild)

    xml_str = root.toprettyxml(indent = "\t")
    #Entfernt die letzte Zeile
    #TODO minidom Alternative suchen
    xml_str = xml_str[:xml_str.rfind('\n')]
    xml_str = xml_str.strip()

    with open('index.xml') as oldIndex:
        if xml_str == oldIndex.read():
            sys.exit(0)
        else:        
            with open('index.xml', 'w') as text_file:
                text_file.write(xml_str)
            sys.exit(1)


rootDir = '../'
exclude = set(['.github', '.git', '.'])
paths = []
productIDs = []

#Durchlaueft alle Ordner außer .github und .git
#Ignoriert alle Dateien, die nicht .xml sind
for subdir, dirs, files in os.walk(rootDir, topdown=True):
    [dirs.remove(d) for d in list(dirs) if d in exclude]

    for file in files:
       filepath = subdir + os.sep + file
       if filepath.endswith('.xml') and not filepath.endswith('index.xml'):
        productID = getProductID(filepath)

        paths.append(filepath)
        productIDs.append(productID)
        
createXML(paths, productIDs)
