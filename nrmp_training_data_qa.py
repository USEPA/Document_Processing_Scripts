import xlsxwriter
import sys
import os
sys.path.insert(1,os.path.join(os.getcwd(),'dependencies')) 
import buildfolder as bf
import datetime
import random
import shutil
from pathlib import Path
import csv
import glob

rootdir = bf.getdrt()

now = datetime.datetime.now()

#delete any existing spreadsheet
for fname in os.listdir(rootdir):
    if fname.startswith("Training Data QA Spreadsheet"):
        os.remove(os.path.join(rootdir, fname))
        print('Existing Spreadsheet Deleted')
        
workbook = xlsxwriter.Workbook(rootdir+'//'+'Training Data QA Spreadsheet'+'_'+now.strftime('%m-%d-%y')+'.xlsx')
worksheet = workbook.add_worksheet("Sheet 1")

qa_files = glob.glob('C:\\Users\\AYuen\\Documents\\Test Training Data Main\\qa_records\\*.txt')
for f in qa_files:
    os.remove(f)
    #print('Files Removed from QA Records Folder')


# Start from the first cell. 
# Rows and columns are zero indexed. 
row1 = 1
col = 0

#get list of files
file_list = []
full_path = []
duplicate_list = []

header_data = ['Filename', 'Record Schedule']
header_format = workbook.add_format({'bold': True,
                                     'bottom': 2,
                                     'bg_color': '#F9DA04'})

for col_num, data in enumerate(header_data):
    worksheet.write(0, col_num, data, header_format)

#check csv for duplicate files
with open('C:\\Users\\AYuen\\Documents\\Test Training Data Main\\previously_qa.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV, None)
    for row in readCSV:
        duplicate_list.append(row[0]) 

csvfile.close()
dupicate_list = set(duplicate_list)

totalfiles = sum([len(files) for r, d, files in os.walk(rootdir)])

threshold = 1000/totalfiles

for root, dirs, files in os.walk(rootdir):
    for file in files:        
        (filename, extension) = os.path.splitext(file)
        
        if '_NRMP' not in filename and '-description' not in filename and '-guidance' not in filename:
            if filename not in duplicate_list:
                src = 'C:\\Users\\AYuen\\Documents\\Test Training Data Main\\Test Training Data\\'
                destination = 'C:\\Users\\AYuen\\Documents\\Test Training Data Main\\qa_records'
                file_list.append(filename)
                full_path.append(root)
                record_schedule = Path(root).parts[6]
                if random.random() < threshold:
                    sourceqa = os.path.join(src, record_schedule, file)
                    #print(file)
                    shutil.copy(sourceqa, destination)
                    worksheet.write(row1, col, file)
                    worksheet.write(row1, col+1, record_schedule)
                    row1 += 1
workbook.close()
print('Spreadsheet Generated')
