import csv
import os
path= 'C:\\Users\\SSchouw\\Environmental Protection Agency (EPA)\\ECMS - Documents\\test nrmp rename\\12-6-19 files.csv'
directoryPath = 'C:\\Users\\sschouw\\Environmental Protection Agency (EPA)\\ECMS - Documents\\Extract Documentum\\Test Training Data'
lstDir = os.walk(directoryPath)
count = 0

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

q = buildq(directoryPath)

# open the .csv file with the csv module
with open(path, 'r') as f:
    csv_file = csv.reader(f)
    # read the new file name from every row 
    for row in csv_file:
        existing_file_name = row[0]
        print(existing_file_name)
        for item in q:
##            for fichero in files:        
##                (filename, extension) = os.path.splitext(fichero)
##                print(filename.find(existing_file_name))
                if item.find(existing_file_name) != -1: # == 0 if contains filename in csv
                    (p,s) = item.split('.')
##                    root_dir = root + '\\'
                    os.rename(item, p+'_NRMP.'+s)
                    count += 1
                    print('total: ' + str(count))
                    print('old: ' +item+ ' new: ' +p+'_NRMP.'+s)
