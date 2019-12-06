import buildfolder as bf
import extractultil as eu
import requests
import os
import re
import shutil

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

if __name__ == "__main__":

    #get source directory
    #get target directory
    #open the logfile
    #build q

    #iterate through q
        #check for similar file name in folder
        #tika extract
        #
    #save directly to target directory

    
    source = bf.getdrt('source')
    target = bf.getdrt('target')

    source_q = bf.buildq(source)
    log = open(os.path.join(target,'logfile.txt'),'w+')
    
    def process(q):
        
        for p,i in enumerate(q):
            content = ''
            filename = i.split('/')[-1]
            savefolder = os.path.join(target,i.split('\\')[-2])

            print('------------Processing :' + i)

            #check if same name file already exists, skip (processing if pdfs-rendition is available)
            if i.lower().endswith('.xml') or i.lower().endswith('.htm'):
                print('Checking Duplicate')
                print(i[:i.index(".")])
                if i[:i.index(".")] in source_q[p-1]:
                    log.write('\nDuplicate File :' + filename)
                    continue                

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
                log.write('\nInvalid type: ' + mime + ', file:' + filename)
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
                log.write('\n Not supported, respond code is: ' + str(resp.status_code) + ", ITEM " + filename + ", TYPE " + mime)
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
                f = filename.split('\\')[-1].split('.')[0]
                t = open(os.path.join(savefolder, f + '.txt'),'wt')
                t.write(eu.cleanMe(content))                                                                                 
                t.close()
                print('content saved to: ' + savefolder)
                log.write('\n Success: ' + filename + ", TYPE " + mime)
            except Exception as e:
                log.write('\nEncountered exception: ' + str(e) + 'at: ' + i)
                fin.close()
                continue
                
            fin.close()

        log.close()

    #process(source_q)
  


