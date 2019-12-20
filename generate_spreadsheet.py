import xlsxwriter
import sys
import os
sys.path.insert(1,os.path.join(os.getcwd(),'dependencies')) 
import buildfolder as bf
import datetime

rootdir = bf.getdrt()

now = datetime.datetime.now()

for fname in os.listdir(rootdir):
    if fname.startswith("Training Data Master Spreadsheet"):
        os.remove(os.path.join(rootdir, fname))
        print('Existing Spreadsheet Deleted')
        
workbook = xlsxwriter.Workbook(rootdir+'//'+'Training Data Master Spreadsheet'+'_'+now.strftime('%m-%d-%y')+'.xlsx')
worksheet = workbook.add_worksheet("Sheet 1")

# Start from the first cell. 
# Rows and columns are zero indexed. 
row = 1
col = 0

header_data = ['Record ID', 'Filename', 'Record Schedule', 'Comments', 'N/A', 'Duplicates']

header_format = workbook.add_format({'bold': True,
                                     'bottom': 2,
                                     'bg_color': '#F9DA04'})

for col_num, data in enumerate(header_data):
    worksheet.write(0, col_num, data, header_format)
    
for folder, subfolders, files in os.walk(rootdir, topdown=False):
   for file in files:
        filePath = os.path.join(folder,file)
        file = filePath.split('\\')[-1]
        recordid = filePath.split('\\')[-2]
        worksheet.write(row, col, recordid)
        worksheet.write(row, col + 1, file)
        row += 1
  
workbook.close()
print('Spreadsheet Generated')
