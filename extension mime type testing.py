import os
import requests
import json
import mimetypes
import magic

directory = os.fsencode("C:\\Users\\AYuen\\Documents\\python script\\python script\\sample")

def tika(files):
    url = 'https://ecms-cis-tika-prod.edap-cluster.com/detect/stream'
    headers = {'Cache-Control': 'no-cache'}
    r = requests.put(url, files=files, headers = headers)
    return r

for file in os.listdir(directory):
     filename = os.fsdecode(file)
     filelocation = directory.decode('utf-8')+"\\"+filename
     file_extension = os.path.splitext(file)[1][1:]
     fin = open(filelocation, 'rb')
     files = {'files':fin}
     r = tika(files)
     mime = magic.Magic(mime=True)
     mimetype = mimetypes.MimeTypes().guess_type(filename)[0]
     #if filename.endswith(".pdf") or filename.endswith(".py"):
     print("libmagic lib: ")
     print(mime.from_file(filelocation))
     print("mimetypes lib: ")
     print(mimetype)
     print("tika lib: ")
     print(r.content.decode('utf-8'))
     print("extension actual: ")
     print(file_extension.decode('utf-8'))
     print("extension guess: ")
     print(mimetypes.MimeTypes().guess_extension(mime.from_file(filelocation)))
     print("-------------------------")
