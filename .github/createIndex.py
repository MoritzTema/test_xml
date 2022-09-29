import os
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
        productChild = root.createElement('ProductID ' + str(id))

        productChild.setAttribute(str(paths[id]), str(IDs[id]))
        xml.appendChild(productChild)

    xml_str = root.toprettyxml(indent = "\t")

    print(xml_str)
    # print('Creating xml...')
    # save_path_file = "../index.xml"

    # with open(save_path_file, "w") as f:
    #     f.write(xml_str)





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

        paths.append([subdir])
        productIDs.append([productID])
        
createXML(paths, productIDs)