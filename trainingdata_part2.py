import sys
import os
sys.path.insert(1,os.path.join(os.getcwd(),'dependencies')) 
import buildfolder as bf
import extractultil as eu
import requests
import re
import shutil
import xlrd


def tika(files):
    url = 'https://ecms-cis-tika.edap-cluster.com/tika/form'
    headers = {'Cache-Control': 'no-cache'}
    r = requests.post(url, files=files, headers = headers)
    return r

def xtika(files):
    url = 'https://ecms-cis-tika.edap-cluster.com/tika'
    headers = {'Content-Type':'application/pdf', 'X-Tika-PDFOcrStrategy': 'ocr_only', 'Cache-Control': 'no-cache'}
    r = requests.put(url, files=files, headers = headers)
    return r

def detect(files):
    
    url = 'https://ecms-cis-tika.edap-cluster.com/detect/stream'
    headers = {'Cache-Control': 'no-cache', 'Content-Type': "false"}
    r = requests.put(url, files=files, headers = headers)
    return r.text

#def checkvalid(mime):
#    filterout = ['mp3','mov','mp4', 'vid', 'cad']
    
def checkvalid(mime):
    filterout = ['aiff','arc','asc','avi','bwf','csi','dbf','ddf','dht','dng','dpx','dqt','e00','ebcdic','flac','gdb','gml','ics','jfif','kml','mbox','mov','mp3','mpeg2','mpeg4','mxf','prc','pst','shp','shx','step','u3d','utf16','utf8','warc','wave','wmv','x3d','x3dv']
    for i in filterout:
        if i in mime:
            return True

    return False

def checkStructure(mime):
    filterout = ['csv', 'xls', 'excel', 'workbook']
    for i in filterout:
        if i in mime:
            return True

    return False

#sourcepath = "C:\\Users\\AYuen\\Environmental Protection Agency (EPA)\\ECMS - Documents\\Extract Documentum\\test extraction 1\\sourcefiles\\"
sourcepath = bf.getdrt()
# Added finalpath which needs to be outside of the sourcefiles directory
#finalpath = "C:\\Users\\AYuen\\Environmental Protection Agency (EPA)\\ECMS - Documents\\Extract Documentum\\test extraction 1\\final\\"
finalpath = bf.getdrt() + '\\'

log = open(os.path.join(finalpath,'logfile.txt'),'w+')

# Change filename if applicable
wb = xlrd.open_workbook("Training Data Master Spreadsheet.xlsx")
sh = wb.sheet_by_index(0)
fd = {}
qq = []

row_value = -1

for cell in sh.col(2):
    row_value += 1
    
    rid = sh.cell(row_value, 0).value
    fnameext = sh.cell(row_value, 1).value
    rschedule = sh.cell(row_value, 2).value
    fname = fnameext.rsplit( ".", 1)[0]
    
    if cell.ctype != xlrd.XL_CELL_EMPTY and fname != "Filename" and rschedule != "Record Schedule":
        fd[fname] = rschedule
    else:
        continue
    
# Get a list of all files under the sourcefiles directory
for (root, dirs, files) in os.walk(sourcepath, topdown=False):
    if len(files) > 0:
        for file in files:
            qq.append(os.path.join(root,file))

#print (fd) Print the dictonary for debugging

# Iterate through all of the files in the sourcfiles directory
for p, i in enumerate(qq):
    # Get filename and filename with no extension
    file = i.split('\\')[-1]
    noext = file.rsplit( ".", 1)[0]

    # Set the savefolder path to the final directory + filename
    try:
        savefolder = finalpath+fd[noext]
    except:
        log.write('\nFile does not exist in spreadsheet: ' + i)
        continue

    # Change Location to reflect where output folders are located
    if not os.path.exists(finalpath+rschedule):
        os.makedirs(finalpath+rschedule)
        print(finalpath+rschedule + " created")

    #copy eml file instead of tika-ing 
    if i.lower().endswith('.eml'):
        shutil.copy(i,savefolder)
        log.write('\nEml file saved: ' + i)
        print('Eml File Saved: ' + i)
        continue
    #setting binary file as json format
    fin = open(i, 'rb')
    files = {'files':fin}

    #detect the mime-type
            
    try: 
        mime = detect(files)
        print('detecting mime type as :' + mime)
    except:
        log.write('\nFailed to detect mime-type ' + i)
        continue
            
    #filter out mp3-like types before proceeding
    if checkvalid(mime):
        log.write('\nInvalid type: ' + mime + ', file:' + file)
        print('Invalid type')
        continue
                                                           

    #resets the binary read start position
    fin.seek(0)

    #call the tika service                                               
    print('beginning Tika service :' + str(p))
    try:
        resp = tika(files)
        content = resp.text
    except:
        log.write('\nTika Failed' + i)
        fin.close()
        continue
            
                
    #if pdf then ocr                                               
    if resp.status_code == 200 and len(resp.text.strip())<1 and 'pdf' in mime:
        print('OCRing PDF')
        fin.seek(0)
        resp = xtika(files)
        content = resp.text
        print('OCRing PDF Finished')                                           

    #if excel or csv type, then truncate
    if checkStructure(mime):
        content = resp.text[:200]
                
    #unsupport type
    if resp.status_code != 200:
        print('Not supported, respond code is:' + str(resp.status_code))
        log.write('\n Not supported, respond code is: ' + str(resp.status_code) + ", ITEM " + file + ", TYPE " + mime)
        fin.close()
        continue

    #create the storage folder            
    if not os.path.exists(savefolder):
        print('made folder ' + savefolder)
        os.mkdir(savefolder)

    #check for none-type
    if resp.text == None:
        log.write('\nWarning, respond text is NoneType, review file :' + i)
        fin.close()
        continue
            
    #final check for length of extracted text'
    if len(resp.text) < 10:
        log.write('\nWarning, text is short, review file :' + i)

    #write the content to file
    try:
    #open the newly created txt file
        t = open(os.path.join(savefolder, noext + '.txt'),'wt')
        #write the output returned from tika endpoint
        t.write(eu.cleanMe(content))
        #close the newly created txt file       
        t.close()
        print('content saved to: ' + savefolder)
        log.write('\n Success: ' + file + ", TYPE " + mime)
    #log any exceptions 
    except Exception as e:
        log.write('\nEncountered exception: ' + str(e) + 'at: ' + i)
        fin.close()
        continue
                
    fin.close()
#close the log 
log.close()
