import buildfolder
import cxwalk
import buildfolder
import os, zipfile

#Old Schedule id must be contained within the name of the zip file
#Unzip file, save to folder of schedule id contained in name of file
if __name__ == "__main__":
    print('Starting Script')
    fail = []

    #get the source/target directory
    source = buildfolder.getdrt('source')
    target = buildfolder.getdrt('target')
    
    #build the folder q
    source_q = buildfolder.buildq(source)
    
    #for each item in q, translate the item, then make the folder
    count = 0
    print(len(source_q))
    fail = open(os.path.join(target,'faillog.txt'),'w+')
    
    for item in source_q: # loop through items in q
        count += 1
        if not item.endswith(".zip"):
            continue
        try:
            zipObj = zipfile.ZipFile(item, 'r')
            print(item)
            try:
                (s,d,f) = cxwalk.translate(item,cxwalk.xwalk)
                foldername = f+"-"+s+"-"+d
            except TypeError:
                foldername = 'No Map'
                fail.write('\nNo Map :'+item+'\n')
                
            savefolder = os.path.join(target,foldername)
            print(savefolder)
            if not os.path.exists(savefolder):
                print('made folder ' + savefolder)
                os.mkdir(savefolder)
            zipObj.extractall(savefolder)
            print('Extracted')
            zipObj.close()
            print(count)
        except:
            try:
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
                print('Failed :' + item)
                zipObj.close()
    fail.close()
