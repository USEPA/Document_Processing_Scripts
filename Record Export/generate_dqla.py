import xlrd
import random
import datetime
import math

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
    total = sh.nrows
    floor = math.floor(total/1000)

    if floor>0:
        for i in range(0,floor+1):
            lanidlist.append([])
            recordlist.append([])

    with open("Records_Export_"+date+"_"+sheet+".csv",'wt', encoding="utf-8") as fs:
        fs.write('Lan_ID,Organization,Record_ID\n')
        count = 0
        for row in rows:
            
            lanid = row[0].value
            recordid = row[1].value
            organization = row[3].value

            
            if floor > 0:
                fl = math.floor(count/1000)
                recordlist[fl].append(recordid)
                if lanid not in lanidlist[fl]:
                    lanidlist[fl].append(lanid)
                    
            else:
                recordlist.append(recordid)
                if lanid not in lanidlist:
                    lanidlist.append(lanid)

            fs.write(str(lanid) + ',' + str(organization) + ',' + str(recordid) +'\n')
            count += 1
            
    fs.close()


    if floor > 0:

        for i in range(0,floor+1):
            print(i)
            mini = i
            maxi = i+1

            text_file1 = open("lanid_" +date + "_" + sheet + "_part_" + str(i)+".txt", "w", encoding="utf-8")
            text_file1.write(str(', '.join(lanidlist[i])))
            text_file1.close()

        
            text_file2 = open("recordid_" + date + "_" + sheet+ "_part_" + str(i) + ".txt", "w", encoding="utf-8")
            text_file2.write("select r_object_id, i_retainer_id from erma_doc where erma_doc_id IN "+str(recordlist[i]).replace('[','(').replace(']',')')) 
            text_file2.close()

    else:
            text_file1 = open("lanid_" +date + "_" + sheet + ".txt", "w", encoding="utf-8")
            text_file1.write(str(', '.join(lanidlist)))
            text_file1.close()

            text_file2 = open("recordid_" + date + "_" + sheet + ".txt", "w", encoding="utf-8")
            text_file2.write("select r_object_id, i_retainer_id from erma_doc where erma_doc_id IN "+str(recordlist).replace('[','(').replace(']',')')) 
            text_file2.close()
