import sys 
sys.path.insert(1,os.path.join('\'.join(os.getcwd().split('\')[:-1]),'dependencies')) 
import os
import shutil
import buildfolder as bf

textfile=bf.getdrt('text')
source = bf.getdrt('source')
target=bf.getdrt('target')

text_q = bf.buildq(textfile)

source_q = bf.buildq(source)

txt_filename = 0
original_filename = 0
number_of_characters = 0

for i in text_q:

    #open text files and read the character count
    file = open(i, "r")
    data = file.read()
    number_of_characters = len(data)

    txt_filename = (os.path.splitext(os.path.basename(i))[0])

    #if character count < 50, copy original files to new folder
    if number_of_characters < 50:
    
        for item in source_q:
            savefolder = os.path.join(target,i.split('\\')[-2])
        
            if not os.path.exists(savefolder):
                print('made folder ' + savefolder)
                os.mkdir(savefolder)
        
            original_filename = (os.path.splitext(os.path.basename(item))[0])
            original_filename2 =(os.path.basename(item))
        
            if txt_filename == original_filename:
                print('processing ' + original_filename2 + ', number of characters = ' + str(number_of_characters))
                shutil.copy(item, savefolder)
    
