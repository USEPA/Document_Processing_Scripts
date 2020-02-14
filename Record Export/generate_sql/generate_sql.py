import xlrd
import math

print('This Module read from the \'Categorization Record Request.xlsx\' \nand generate multiple sql \nstatements for exporting records information. \nResults are written to sql_text.txt') 

      
wb = xlrd.open_workbook("Categorization Record Request.xlsx")
sh = wb.sheet_by_index(0)

rows = sh.get_rows()
total = sh.nrows

sql_1 = "select s.ERMA_DOC_CUSTODIAN,s.ERMA_DOC_ID,s.ERMA_DOC_TITLE,group_name from ECMSRMR65.ERMA_DOC_SV s where "
sql_2 = "lower(group_name) like "



gen = {}
sql_text = open('sql_text.txt','wt')

for i in range(1,total):

    try:
        num = round(sh.row(i)[2].value)
        org = str(sh.row(i)[1].value.strip().lower())
    except TypeError:
        break
    if num in gen.keys():
        gen[num].append(org)
    else:
        gen[num] = [org]        

for key in gen.keys():
    count = 0
    sql = sql_1
    
    for item in gen[key]:

        count += key
        sql += sql_2 + '\'%'+str(item)+'%\'' + ' or '

        if count%1000 == 0:
            
            sql = sql[:-3] + f'order by dbms_random.value fetch first 1000 rows only;'    
            sql_text.write(sql+'\n')

            sql = sql_1
            count = 0

            continue

    sql = sql[:-3] + f'order by dbms_random.value fetch first {count%1000} rows only;'    
    sql_text.write(sql+'\n')


sql_text.close()
