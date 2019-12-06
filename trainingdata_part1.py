import os
import shutil
# from shutil import copyfile

# Change basepath if applicable
basepath = "C:\\Users\\AYuen\\Environmental Protection Agency (EPA)\\ECMS - Documents\\Categorization Data\\"
copypath = "C:\\Users\\AYuen\\Environmental Protection Agency (EPA)\\ECMS - Documents\\newfiles\\"

# Get all files in the directory
qq = []

for (root, dirs, files) in os.walk(basepath, topdown=False):
    if len(files) > 0:
        for file in files:
            qq.append(os.path.join(root,file))

for filename in qq:
    # Get the filename
    file = filename.split('\\')[-1]
    # For ezEmail, if file is in the pdf folder extract record ID from end of filename
    if 'pdf' in filename and 'attachment' not in filename:
        print(file.rsplit( ".", 1)[0].rsplit('_', 1)[1])
        recordid = file.rsplit( ".", 1)[0].rsplit('_', 1)[1]
        if not os.path.exists(copypath+recordid):
            os.makedirs(copypath+recordid)
        if recordid in filename:
            # copyfile(filename, copypath+recordid+'\\'+file)
            shutil.move(filename, copypath+recordid+'\\'+file)  
    # For ezEmail, if file is in the pdf folder extract record ID from begining of filename
    if 'attachment' in filename:
        print(file.rsplit( ".", 1)[0].rsplit('_')[0])
        recordid = file.rsplit( ".", 1)[0].rsplit('_')[0]
        if not os.path.exists(copypath+recordid):
            os.makedirs(copypath+recordid)
        if recordid in filename:
            # copyfile(filename, copypath+recordid+'\\'+file)
            shutil.move(filename, copypath+recordid+'\\'+file)
    # For ezDesktop records grab the record at the root of the LAN ID folder
    if 'desktop' in filename:
        print(file.rsplit( ".", 1)[0].rsplit('_', 1)[1])
        recordid = file.rsplit( ".", 1)[0].rsplit('_', 1)[1]
        if not os.path.exists(copypath+recordid):
            os.makedirs(copypath+recordid)
        if recordid in filename:
            # copyfile(filename, copypath+recordid+'\\'+file)
            shutil.move(filename, copypath+recordid+'\\'+file)

