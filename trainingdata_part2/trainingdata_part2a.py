import sys 
sys.path.insert(1,os.path.join('\'.join(os.getcwd().split('\')[:-1]),'dependencies')) 
import buildfolder as bf
import extractultil as eu
import requests
import os
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

def checkvalid(mime):
    filterout = ['mp3','mov','mp4', 'vid', 'cad']
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

basepath = "C:\\Users\\AYuen\\Environmental Protection Agency (EPA)\\ECMS - Documents\\Extract Documentum\\test extraction 1"
sourcepath = "C:\\Users\\AYuen\\Environmental Protection Agency (EPA)\\ECMS - Documents\\Extract Documentum\\test extraction 1\\sourcefiles\\"
# Added finalpath which needs to be outside of the sourcefiles directory
finalpath = "C:\\Users\\AYuen\\Environmental Protection Agency (EPA)\\ECMS - Documents\\Extract Documentum\\test extraction 1\\final\\"
log = open(os.path.join(finalpath,'logfile.txt'),'w+')

# Change filename if applicable
wb = xlrd.open_workbook("trainingdata_part2.xlsx")
sh = wb.sheet_by_index(0)
fd = {}
qq = []

rows = sh.get_rows()
# Skip header row
next(rows)

for row in rows:
    # Extract value from spreadsheet and save to variable
    rid = row[0].value
    rschedule = row[2].value
    fnameext = row[1].value
    fname = fnameext.rsplit( ".", 1)[0]
    # Assign filename and schedule as key value pair to dictonary
    fd[fname] = rschedule
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
    savefolder = finalpath+fd[noext]
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
