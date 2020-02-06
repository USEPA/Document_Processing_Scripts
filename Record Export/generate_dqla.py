import xlrd
import random
import datetime

wb = xlrd.open_workbook("Record IDs.xlsx", on_demand=True)
res = len(wb.sheet_names())

for s in range(0,res):

    sh = wb.sheet_by_index(s)
    
    rows = sh.get_rows()

    # Skip header row
    next(rows)
    
    lanidlist = []
    recordlist = []

    date = str(datetime.date.today())
    sheet = str(s)

    with open("Records_Export_"+date+"_"+sheet+".csv",'wt', encoding="utf-8") as fs:
        fs.write('Lan_ID,Organization,Record_ID\n')
    
        for row in rows:

            lanid = row[0].value
            recordid = row[1].value
            organization = row[3].value
            
            recordlist.append(recordid)
            
            if lanid not in lanidlist:
                lanidlist.append(lanid)

            fs.write(str(lanid) + ',' + str(organization) + ',' + str(recordid) +'\n')

    fs.close()

    with open("lanid_"+date+"_"+sheet+".txt", "w", encoding="utf-8") as text_file1:
        text_file1.write(str(', '.join(lanidlist)))


    with open("recordid_"+date+"_"+sheet+".txt", "w", encoding="utf-8") as text_file2:
        text_file2.write("select r_object_id, i_retainer_id from erma_doc where erma_doc_id IN "+str(recordlist).replace('[','(').replace(']',')')) 

    text_file1.close()
    text_file2.close()  
