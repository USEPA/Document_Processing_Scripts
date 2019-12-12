import os, zipfile, fnmatch
import magic


#import the dependencies
import sys
sys.path.insert(1,os.path.join(os.getcwd(),'dependencies')) #or folder name

import buildfolder as bf
import cxwalk as cx

#xwp = r'C:\Users\mnguyen\Environmental Protection Agency (EPA)\ECMS - Documents\github\Document_Processing_Scripts\dependencies\xwalk.csv'
xwalk = cx.make_xwalk(os.path.join(sys.path[1],'xwalk.csv'))

#get the source and target directory
source = bf.getdrt('source')
target = bf.getdrt('target')

#build the folder q
source_q = bf.buildq(source)

fail = open(os.path.join(target,'faillog.txt'),'w+')

#loop through items in q
for item in source_q:
    #get the extension of files
    mime = magic.Magic(mime=True)
    extension = (os.path.splitext(os.path.basename(item)))

    #if mime type is detected as zip then rename extension to .zip
    if mime == 'application/zip':
        if extension != '.zip':
            os.rename(item, extension + '.zip')
    
    try:
        #create a folder to save all extracted files to
        f,s,d = cx.translate(item.split('\\')[-2],xwalk)
        newcode = f+'-'+s+'-'+d
        savefolder = os.path.join(target, newcode)
        
        if not os.path.exists(savefolder):
            print('Made folder: ' + savefolder)
            os.mkdir(savefolder)

        #create a zip object and extract all files to the target folder
        zipObj = zipfile.ZipFile(item, 'r')
        zipObj.extractall(savefolder)
        print(item + ': extracted')
        zipObj.close()
    except:
        try:
            #if file could not be processed, write to faillog
            zipObj = zipfile.ZipFile(item, 'r')
            zipinfos = zipObj.infolist()
            print('Processing exception')
            for zipinfo in zipinfos:
                zipinfo.filename = re.sub('[\t ]+', ' ', zipinfo.filename)
                zipObj.extract(zipinfo,savefolder)
                print('exception processed')
                zipObj.close()
        except:
            fail.write('\n'+item+'\n')
            print('Failed : ' + item)
            zipObj.close()
fail.close()
