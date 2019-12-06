import os
import xlsxwriter

# Change basepath if applicable
basepath = "C:\\Users\\AYuen\\Environmental Protection Agency (EPA)\\ECMS - Documents\\newfiles\\"

workbook = xlsxwriter.Workbook(basepath+'fileandid.xlsx')
worksheet = workbook.add_worksheet("Sheet 1")

# Start from the first cell. 
# Rows and columns are zero indexed. 
row = 0
col = 0

# Get all files in the directory
qq = []

for (root, dirs, files) in os.walk(basepath, topdown=False):
    if len(files) > 0:
        for file in files:
            qq.append(os.path.join(root,file))

print(qq[1])

for item in qq:
    rid = item.split('\\')[6]
    fname = item.split('\\')[7]
    print(f'record id is {rid}')
    print(f'file name is {fname}')    
    worksheet.write(row, col, rid) 
    worksheet.write(row, col + 1, fname) 
    row += 1
  
workbook.close()
