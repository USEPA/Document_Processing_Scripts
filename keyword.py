from rake_nltk import Rake
from bs4 import BeautifulSoup
import sys
import os
sys.path.insert(1,os.path.join(os.getcwd(),'dependencies')) 
import buildfolder as bf
import datetime
import xlsxwriter
import xlrd
import csv

#select location where keywords.xlsx exists and where it will write the final resulting spreadsheet.
rootdir = bf.getdrt()
now = datetime.datetime.now()

#delete any existing spreadsheet
for fname in os.listdir(rootdir):
    if fname.startswith("Keyword Spreadsheet"):
        os.remove(os.path.join(rootdir, fname))
        print('Existing Spreadsheet Deleted')
        
workbook = xlsxwriter.Workbook(rootdir+'//'+'Keyword Spreadsheet'+'_'+now.strftime('%m-%d-%y')+'.xlsx')
worksheet = workbook.add_worksheet("Sheet 1")

# Start from the first cell. 
# Rows and columns are zero indexed. 
row1 = 1
col = 0

#get list of files
file_list = []
full_path = []
duplicate_list = []

header_data = ['ID', 'Record_Schedule_Number', 'Combine_Description', 'Keywords']
header_format = workbook.add_format({'bold': True,
                                     'bottom': 2,
                                     'bg_color': '#F9DA04'})

for col_num, data in enumerate(header_data):
    worksheet.write(0, col_num, data, header_format)

wb = xlrd.open_workbook("keywords.xlsx")
sh = wb.sheet_by_index(0)

rows = sh.get_rows()
# Skip header row
next(rows)

for row in rows:
    # Extract value from spreadsheet and save to variable
    db_id = row[0].value
    rs_num = row[1].value
    description = row[2].value

    r = Rake(min_length=2, max_length=3) # Uses stopwords for english from NLTK, and all puntuation characters.

    soup = BeautifulSoup(description, 'html.parser')

    #print(soup.get_text())

    r.extract_keywords_from_text(soup.get_text())

    keywords = r.get_ranked_phrases() # To get keyword phrases ranked highest to lowest.

    #print(r.get_ranked_phrases_with_scores())
    worksheet.write(row1, col, db_id)
    worksheet.write(row1, col+1, rs_num)
    worksheet.write(row1, col+2, str(keywords))
    row1 += 1
    
workbook.close()
print('Spreadsheet Generated')
