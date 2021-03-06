import string
import time
import sys
import os
sys.path.insert(1,os.path.join(os.getcwd(),'dependencies')) 
import buildfolder as bf
import shutil
import random
import re

#### COMMENT THIS OUT TOO
#stdoutOrigin=sys.stdout 
#sys.stdout = open("log.txt", "w")

sourcepath = bf.getdrt()
finalpath = bf.getdrt() + '\\'

def remove_punc(str):
    return re.sub("\d+", " ",''.join(c for c in str if c not in punctuation))

def removesmallchar(sourcepath, finalpath=finalpath):
     sourcepath = sourcepath
     finalpath = finalpath 
     directory = "smallfiles"
     destpath = os.path.join(finalpath + directory)
     
     if not os.path.exists(destpath):
            print('made folder ' + destpath)
            os.mkdir(destpath)
     for root, dirs, files in os.walk(sourcepath):
          for file in files:
             try:
                 infile=open(os.path.join(root, file), 'r', encoding="utf8", errors='ignore')
             except OSError:
                 print("Could not open/read file:", file)
                 #os.remove(os.path.join(root, file))
                 continue
             lines=0
             words=0
             characters=0
             for line in infile:
                 line = line.strip(os.linesep)
                 wordslist=line.split()
                 lines=lines+1
                 words=words+len(wordslist)
                 characters=characters+ len(line)
             infile.close()
             if characters < 355 and "-description" not in file:
                 shutil.move(os.path.join(root, file),destpath)
                 print('Moved file: ' + os.path.join(root, file))
                 
def move_file(i,finalpath=finalpath):                
    # Set the savefolder path to the final directory + filename
    try:
        savefolder = finalpath+i.split('\\')[-2]
        if not os.path.exists(savefolder):
            print('made folder ' + savefolder)
            os.mkdir(savefolder)
        shutil.move(i, savefolder)
        print('bad file detected - moved')
    except:
        return 0

start = time.time()

punctuation = set(string.punctuation)

#### COMENT THIS OUT AS WELL
# Move all files with <355 characters into the smallfiles folder for review
removesmallfiles = removesmallchar(sourcepath)

qq = []

# Get a list of all files under the sourcepath directory
for (root, dirs, files) in os.walk(sourcepath, topdown=False):
    if len(files) > 0:
        for file in files:
            qq.append(os.path.join(root,file))

count = 0
## START COMMENTING OUT HERE
# Iterate through all of the files in the sourcfiles directory
for p, i in enumerate(qq[2901:]): #set the counter here enumerate(qq[start:]):   example enumerate(qq[5:]):

##    To determine position run the following in the shell:
##        for p,i in enumerate(qq):
##	if 'insert filename of last file here' in i:
##		print(p)
##		break
	    
    # Get filename and filename with no extension
    file = i.split('\\')[-1]
    noext = file.rsplit( ".", 1)[0]

    eng_words = open("words.txt").readlines()
    eng_words = [w.strip().lower() for w in eng_words]
    eng_words = set(eng_words)
    total_count = 0
    eng_count = 0

    try:
        filesize = os.path.getsize(i)
    except OSError:
        print("Could not open/read file:", i)
        continue
    #with open(i, encoding="utf8") as f:
    with open(i, encoding="utf8", errors='ignore') as f:
        for line in f:
            try:
                # Check if file is greater than 60kb and randomly select lines to review to reduce overall processing time.
                if filesize > 50000:
                    if random.random() < .5:
                        continue
                words = remove_punc(line).lower().split()
                wordlist = words
                for item in wordlist:
                        try:
                            # Remove numbers from processing.
                            if item.isnumeric():
                                words.remove(item)
                        except ValueError:
                            continue
                #print(words)
                total_count += len(words)
                eng_count += sum(1 for word in words if word.lower() in eng_words)
            except OSError:
                print("Could not open/read file:", file)
                #os.remove(os.path.join(root, file))
                continue 
            
    print (f'---------item {count} ------------')
    print ('%s English words found' % eng_count)
    print ('%s total words found' % total_count)

    percentage_eng = 0 if total_count == 0 else (float(eng_count) / total_count * 100)
    print ('%s%% of words were English' % percentage_eng)

    finish = time.time()
#
    total = finish-start

    print(f'File Size in bytes: {filesize}')
    print('Filename: '+i.split('\\')[-1])
    print(f'{total} seconds')

    # Set the threshold levels where files are deemed in need of review and move those files to finalpath.
    #add ocr issue message
    if 1 <= eng_count <= 300:
        if percentage_eng < 51:
            move_file(i)
    if 301 <= eng_count <= 500:
        if percentage_eng < 55:
            move_file(i)
    elif 501 <= eng_count <= 5000:
        if percentage_eng < 60:
            move_file(i)
    elif 5001 <= eng_count > 10000:
        if percentage_eng < 65:
            move_file(i)       
    count += 1
#sys.stdout.close()
#sys.stdout=stdoutOrigin
