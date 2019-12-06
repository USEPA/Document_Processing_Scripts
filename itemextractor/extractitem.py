import xlsxwriter,xlrd,os,re

# Change basepath if applicable
basepath = "C:\\Users\\AYuen\\Environmental Protection Agency (EPA)\\ECMS - Documents\\Extract Documentum\\itemextractor\\"
workbook = xlsxwriter.Workbook(basepath+'item_descriptions.xlsx')
worksheet = workbook.add_worksheet("Item Desc")

wb = xlrd.open_workbook(basepath+'all_schedules.xlsx')
sh = wb.sheet_by_index(0)

# Overall Content Array
content_array  = []

for row in sh.get_rows():
    # Extract value from spreadsheet and save to variable
    itemid = row[1].value
    schedule = row[0].value
    folder = row[3].value
    
    # Array for extracted item description
    data=[]
    flag=False
    with open(basepath + 'data\\' + schedule + '.txt','r', encoding='utf-8',
                 errors='ignore') as f:
        for line in f:
            if line.startswith('Item ' + itemid +':'):
                data.append(line)
                flag=True
                continue
            # Use Regex to find the begining of the next item
            r = re.compile('Item .*:')            
            if  re.match(r, line.strip()):
                flag=False
            # Search for guidance (Last of the items)
            if 'Guidance:' in line.strip():
                flag=False
                
            if flag:
                data.append(line)                

    print(''.join(data))
    content = ''.join(data)
    
    content_array.append([folder,content])
    print('-----')
    
print(content_array)
    
# Start from the first cell. 
# Rows and columns are zero indexed. 
row = 0
col = 0

# Iterate over the data and write it out row by row. 
for name, content in (content_array): 
    worksheet.write(row, col, name) 
    worksheet.write(row, col + 1, content) 
    row += 1
  
workbook.close()
