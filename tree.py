from __future__ import print_function
import os, os.path
from xml.dom.minidom import Document
import datetime
import MySQLdb

dbip = 'localhost'
dbuser = 'root'
dbpass = '1'
dbname = 'tree'
db = MySQLdb.connect(dbip,dbuser,dbpass,dbname)
cursor = db.cursor()

log = open('/home/russel/DEV/py/tree_builder/log.xml', 'w')
# doc = Document()

# def makenode(path):
#     # "Return a document node contains a directory tree for the path."
#     node = doc.createElement('dir')
#     nodetext = doc.createTextNode(path)
#     node.appendChild(nodetext)
#     for f in os.listdir(path):
#         fullname = os.path.join(path, f)
#         if os.path.isdir(fullname):
#             elem = makenode(fullname)
#         else:
#             elem = doc.createElement('file')
#             nodetext = doc.createTextNode(f)
#             elem.appendChild(nodetext)
#             elem.setAttribute('path', fullname)
#         node.appendChild(elem)
#     return node

# doc.appendChild(makenode('/home/russel/djcode/slideshow'))
# print(doc.toprettyxml(), file=log)

# doc = Document()
# parentpath = ''
# def makenode(path):
#     # "Return a document node contains a directory tree for the path."
#     node = doc.createElement('item')
#     node.setAttribute('id', path)
#     nodecontent = doc.createElement('content')
#     node.appendChild(nodecontent)
#     nodename = doc.createElement('name')
#     nodecontent.appendChild(nodename)
#     nodetext = doc.createTextNode(path)
#     nodename.appendChild(nodetext)
#     for f in os.listdir(path):
#         fullname = os.path.join(path, f)
#         if os.path.isdir(fullname):
#             elem = makenode(fullname)
#         else:
#             elem = doc.createElement('item')
#             elem.setAttribute('parent_id', path)
#             nodecontent = doc.createElement('content')
#             elem.appendChild(nodecontent)
#             nodename = doc.createElement('name')
#             nodecontent.appendChild(nodename)
#             nodetext = doc.createTextNode(f)
#             nodename.appendChild(nodetext)
#             # nodename.setAttribute('path', fullname)
#             # nodename.setAttribute('file', 'yes')
#         node.appendChild(elem)
#     return node

# doc.appendChild(makenode('/home/russel/DEV/py/tree_builder/test_folder'))
# print(doc.toprettyxml(), file=log)


doc = Document()
parentpath = ''

sql = "SELECT path FROM tree.testtree" 
cursor.execute(sql)
base = cursor.fetchall()
lines = []
for line in base:
    lines += line
lines.sort()
# print(lines[:10])
# for line in file:
#     print(line)
path = '/data/share/production/ShowMustGoOn/Arxiv_Dnevniki/02/.AppleDouble'


def getChild(path):
    childs = []
    for line in lines:
        if path in line and len(line) != len(path):
            path_splitted = path.split('/')
            line_splitted = line.split('/')
            new_path = ''
            for item in line_splitted[1:len(path_splitted)+1]:
                new_path += '/' + item
            if new_path not in childs:
                childs.append(new_path)
                
    return childs
# print(getChild(path))

def isdir(path):
    if (path.split('/')[-1].find('.')==0 or path.split('/')[-1].find('.')==-1):
        return True
    else:
        return False
# print(isdir(path))


def makenode(path):
    # "Return a document node contains a directory tree for the path."
    node = doc.createElement('item')
    node.setAttribute('id', path)
    node.setAttribute('rel', 'folder')
    nodecontent = doc.createElement('content')
    node.appendChild(nodecontent)
    nodename = doc.createElement('name')
    nodecontent.appendChild(nodename)
    nodetext = doc.createTextNode(path.split('/')[-1])
    nodename.appendChild(nodetext)
    child_list = getChild(path)
    for f in child_list:
        # print(f)
        if isdir(f):
            elem = makenode(f)
        else:
            elem = doc.createElement('item')
            elem.setAttribute('parent_id', path)
            elem.setAttribute('id', f)
            elem.setAttribute('rel', 'file')
            nodecontent = doc.createElement('content')
            elem.appendChild(nodecontent)
            nodename = doc.createElement('name')
            nodecontent.appendChild(nodename)
            nodetext = doc.createTextNode(f.split('/')[-1])
            nodename.appendChild(nodetext)
            # nodename.setAttribute('path', fullname)
            # nodename.setAttribute('file', 'yes')
        node.appendChild(elem)
    return node

# doc.appendChild(
doc.appendChild(makenode('/data/share/production/ShowMustGoOn'))

print(doc.toprettyxml(), file=log)