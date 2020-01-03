### Track the count
##

import os
import sys

sys.path.insert(1,os.path.join('\\'.join(os.getcwd().split('\\')[:-1]),'dependencies'))

import dctmdl as dd
import buildfolder as bf

#destination = r'C:\Users\mnguyen\Desktop\test'
destination = bf.getdrt()
#sourcelist = r'C:\Users\mnguyen\Environmental Protection Agency (EPA)\ECMS - Documents\github\Document_Processing_Scripts\Dwl Obj by ID from Schedule\objid.csv'
sourcelist = 'objid.csv'

import csv
import logging

logger = logging.getLogger(__name__)
#except:
#    logging.basicConfig(filename='download')

#with open(sourcelist, newline='') as csvfile:
    #reader = csv.reader(csvfile, delimiter=',')

csvfile = open(sourcelist, newline='')
reader = csv.reader(csvfile, delimiter=',')
count = 0

#stopped at 80,000
for row in reader:
    count +=1
    if count <40000: #Continue from
        continue
    if count == 80000: #End at
        break
    
    try:
        r = dd.getpackage(row[0])
        h = r.headers['Content-Disposition'][22:-1]
        if not os.path.exists(destination + '\\' + row[1]):
            os.mkdir(destination + '\\' + row[1])
        f = open(destination + '\\' + row[1] + '\\' + h, 'wb')
        f.write(r.content)
        f.close()
        print(f'success {count} : {row[0]}')

    except:
        logger.warning(f'failed: {row[0]}')
        print(f'fail {count} : {row[0]}')

