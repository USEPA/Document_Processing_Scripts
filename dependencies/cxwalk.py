#call makexwalk() to create the xwalk dictionary
#pass the dictionary to the trasnlate function

import re, string
import csv
import os

#xwalkpath = os.path.join(os.getcwd(),'xwalk.csv')
#xwp = r'C:\Users\mnguyen\Environmental Protection Agency (EPA)\ECMS - Documents\github\Document_Processing_Scripts\dependencies'
xwalk = {}

def make_xwalk(file='xwalk.csv'):
    #TODO importing this from another module breaks the path to the csv. Rewrite to find the xwalkcsv path
    d = {}
    p = re.compile('[\W_]+')
    with open(file,newline='') as f:
        spam = csv.reader(f,delimiter=',')
        for row in spam:
            d[p.sub('',row[0]+row[1])] = (row[2],row[3],row[4])
    return d

#xwalk = make_xwalk()       
#name as full schedule code
def snipcode(name):
    b = re.compile('\d{3}')
    begin = b.search(name).span()[0]
    name = name[begin:]

    e = re.compile('_[a-z]{1}[\(]{0,1}[\d]?[\)]?\(?\d?\)?')
    end = e.search(name).span()[1]
    name = name[:end]
    
    function = name.split('-')[0]
    schedule = name.split('_')[1]
    item = name.split('_')[2]

    if len(item) >1:
        if '(' not in item:
            item = item[:1]
        else:
            item = item.replace('(','')
            item = item.replace(')','')
            
    return (function.strip(), schedule.strip(), item.strip())
                

def translate(name, xwalk=xwalk):
    if len(xwalk) == 0:
        raise Exception('call make_xwalk() first, pass xwalk into this function')
    (f,s,d) = snipcode(name)

    try:
        s1,d1,f1 = xwalk[s+d] 
        if s1 == '':
            return('0'+s,'a',f)
        return (f1,s1,d1)    
    except KeyError:
        return 'none'




