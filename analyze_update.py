import string
import time
import sys
import os
sys.path.insert(1,os.path.join(os.getcwd(),'dependencies')) 
import buildfolder as bf
import shutil
import random

sourcepath = bf.getdrt()
finalpath = bf.getdrt() + '\\'

def remove_punc(str):
    return ''.join(c for c in str if c not in punctuation)

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
             infile=open(os.path.join(root, file), 'r')
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
             if characters < 355:
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

# Move all files with <355 characters into the smallfiles folder for review
removesmallfiles = removesmallchar(sourcepath)

qq = []

# Get a list of all files under the sourcepath directory
for (root, dirs, files) in os.walk(sourcepath, topdown=False):
    if len(files) > 0:
        for file in files:
            qq.append(os.path.join(root,file))

count = 0

# Iterate through all of the files in the sourcfiles directory
for p, i in enumerate(qq): #set the counter here enumerate(qq[start:]):   example enumerate(qq[5:]): 
    # Get filename and filename with no extension
    file = i.split('\\')[-1]
    noext = file.rsplit( ".", 1)[0]

    eng_words = open("words.txt").readlines()
    eng_words = [w.strip().lower() for w in eng_words]

    total_count = 0
    eng_count = 0
    filesize = os.path.getsize(i)
    with open(i) as f:
        for line in f:
            # Check if file is greater than 60kb and randomly select lines to review to reduce overall processing time.
            if filesize > 60000:
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

    print (f'---------item {count} ------------')
    print ('%s English words found' % eng_count)
    print ('%s total words found' % total_count)

    percentage_eng = 0 if total_count == 0 else (float(eng_count) / total_count * 100)
    print ('%s%% of words were English' % percentage_eng)

    finish = time.time()

    total = finish-start

    print(f'File Size in bytes: {filesize}')
    print('Filename: '+i.split('\\')[-1])
    print(f'{total} seconds')

    # Set the threshold levels where files are deemed in need of review and move those files to finalpath.
    if eng_count < 100:
        if percentage_eng < 55:
            move_file(i)
    elif eng_count < 300:
        if percentage_eng < 60:
            move_file(i)
    elif eng_count < 500:
        if percentage_eng < 65:
            move_file(i)
    elif eng_count < 5000:
        if percentage_eng < 70:
            move_file(i)
    elif eng_count > 10000:
        if percentage_eng < 75:
            move_file(i)       
    count += 1
