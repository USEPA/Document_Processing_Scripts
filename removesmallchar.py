import os
import buildfolder as bf

def removesmallchar():
     basepath = bf.getdrt()

     for root, dirs, files in os.walk(basepath):
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
             '''print(file)
             print(lines)
             print(words)
             print(characters)
             print('-----')'''
             infile.close()
             if characters < 355:
                 os.remove(os.path.join(root, file))
                 print('removed file: ' + os.path.join(root, file))
