import os
from tkinter import filedialog
from tkinter import *
from zipfile import ZipFile

#File Queue Builder, return list of all file within a root director
def buildq(rootdir, genfile = 'no'):
    qq = []
    for (root, dirs, files) in os.walk(rootdir, topdown=False):
        if len(files) > 0:
            for file in files:
                qq.append(os.path.join(root,file))

    if genfile.lower() == 'yes':
        with open('folderQ.txt', 'wt') as folderq:
            for i in qq:
                folderq.write(i)
        folderq.close()

    return qq

#Opens the window to select directory as source or target
def getdrt(p=' '):
    if type(p) != str:
        p=' '
        
    root = Tk()
    root.dirname = filedialog.askdirectory(parent=root,initialdir=os.getcwd(),title='Please select a directory as ' + p)
    root.destroy()
    return root.dirname

def makefolder(q):
    for i in q:
        if not os.path.exists(i):
            os.mkdir(i)


