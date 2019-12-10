import os
import sys

sys.path.insert(1,os.path.join('\\'.join(os.getcwd().split('\\')[:-1]),'dependencies'))

import dctmdl as dd
import buildfolder as bf

detination = r'C:\Users\mnguyen\Desktop\test'
sourcelist = r'C:\Users\mnguyen\Environmental Protection Agency (EPA)\ECMS - Documents\github\Document_Processing_Scripts\Dwl Obj by ID from Schedule\objid.csv'

import csv

#with open(sourcelist, newline='') as csvfile:
    #reader = csv.reader(csvfile, delimiter=',')

csvfile = open(sourcelist, newline='')
reader = csv.reader(csvfile, delimiter=',')
count = 1

log = open('downloadlog.txt','wt')

for row in reader:
    try:
        r = dd.getpackage(row[0])
        h = r.headers['Content-Disposition'][22:-1]
        if not os.path.exists(detination + '\\' + row[1]):
            os.mkdir(detination + '\\' + row[1])
        f = open(detination + '\\' + row[1] + '\\' + h, 'wb')
        f.write(r.content)
        f.close()
        log.write(f'success: {row[0]}' + '\n')
        print(f'finsihed downloading {count} file with objid {row[0]}')

    except:
        log.write(f'failed: {row[0]}' + '\n')
        print(f'failed: {row[0]}')

