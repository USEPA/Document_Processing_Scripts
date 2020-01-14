import xlrd

wb = xlrd.open_workbook("Record IDs.xlsx")
sh = wb.sheet_by_index(0)

rows = sh.get_rows()
lanidlist = []
recordlist = []

for row in rows:
    
    lanid = row[1].value
    recordid = row[0].value

    recordlist.append(recordid)
        
    if lanid not in lanidlist:
        lanidlist.append(lanid)

with open("lanid.txt", "w") as text_file1:
    text_file1.write(str(','.join(lanidlist)))


with open("recordid.txt", "w") as text_file2:
    text_file2.write("select r_object_id, i_retainer_id from erma_doc where erma_doc_id IN "+str(recordlist).replace('[','(').replace(']',')')) 

