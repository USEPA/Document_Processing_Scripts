import xlrd
import os
import shutil

#def replace_with_underscores(cell):
#    return cell.value.replace(" ", "_")

basepath = "E:\\TRAINING DATA FOR DEEP DETECT\\"
# Change filename if applicable
wb = xlrd.open_workbook("QA_Spreadsheet.xlsx")
sh = wb.sheet_by_index(0)


rows = sh.get_rows()
# Skip header row
next(rows)


for row in rows:
    # Extract value from spreadsheet and save to variable
    filename = row[0].value
    old = row[1].value
    new = row[2].value
    source = basepath+old+'\\'+filename
    destination = basepath+new+'\\'+filename
    
    if new == 'delete':
        os.remove(source)
        print(filename + " removed")
        
    elif os.path.exists(basepath+old+'\\'+filename):
        dest = shutil.move(source, destination)
        print(filename + " moved")
    else:
        print(filename + " --error--")
