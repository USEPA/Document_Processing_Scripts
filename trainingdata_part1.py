import os
import shutil
# from shutil import copyfile

# Change basepath if applicable
basepath = "C:\\Users\\AYuen\\Environmental Protection Agency (EPA)\\ECMS - Documents\\Categorization Data\\"
copypath = "C:\\Users\\AYuen\\Environmental Protection Agency (EPA)\\ECMS - Documents\\newfiles\\"

# Get all files in the directory
qq = []

# Check for unwanted file extensions
filterout = ['mp3','mov','mp4', 'vid', 'cad']

for (root, dirs, files) in os.walk(basepath, topdown=False):
    if len(files) > 0:
        for file in files:
            qq.append(os.path.join(root,file))

for filename in qq:
    # Get the filename
    file = filename.split('\\')[-1]
    fileext = filename.split(".")[-1]
    # For ezEmail - email content, if file is in the pdf folder extract record ID from end of filename
    if 'pdf' in filename and 'attachment' not in filename and fileext.lower() not in filterout:
        print(file.rsplit( ".", 1)[0].rsplit('_', 1)[1])
        recordid = file.rsplit( ".", 1)[0].rsplit('_', 1)[1]
        if not os.path.exists(copypath+recordid):
            os.makedirs(copypath+recordid)
        if recordid in filename:
            # copyfile(filename, copypath+recordid+'\\'+file)
            shutil.move(filename, copypath+recordid+'\\'+file)  
    # For ezEmail - attachment, if file is in the attachment folder extract record ID from begining of filename
        continue
    if 'attachment' in filename and fileext.lower() not in filterout:
        print(file.rsplit( ".", 1)[0].rsplit('_')[0])
        recordid = file.rsplit( ".", 1)[0].rsplit('_')[0]
        if not os.path.exists(copypath+recordid):
            os.makedirs(copypath+recordid)
        if recordid in filename:
            # copyfile(filename, copypath+recordid+'\\'+file)
            shutil.move(filename, copypath+recordid+'\\'+file)
    # For ezDesktop records grab the record in the desktop folder extract record ID from end of filename
        continue
    if 'desktop' in filename and fileext.lower() not in filterout:
        print(file.rsplit( ".", 1)[0].rsplit('_', 1)[1])
        recordid = file.rsplit( ".", 1)[0].rsplit('_', 1)[1]
        if not os.path.exists(copypath+recordid):
            os.makedirs(copypath+recordid)
        if recordid in filename:
            # copyfile(filename, copypath+recordid+'\\'+file)
            shutil.move(filename, copypath+recordid+'\\'+file)
        continue
