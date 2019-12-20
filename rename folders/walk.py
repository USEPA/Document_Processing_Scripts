import sys
import os
import buildfolder as bf

rootdir = bf.getdrt()

for root, dirs, files in os.walk(rootdir, topdown=False):
   for name in dirs:
      #removes the first 8 characters from the folder name
      newname = name[8:]
      os.rename(os.path.join(root, name),os.path.join(root, newname))
      print(newname)
