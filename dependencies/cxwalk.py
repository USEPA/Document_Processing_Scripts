#crosswalk as key-value dictionary
#parse left to right, split by non-alphanumeric character, store all number
#function is first number
#last number is schedule, and position of lastnumber +1 is deposition

import re, string
import csv
import os

xwalkpath = os.path.join(os.getcwd(),'xwalk.csv')
xwalk = {}

def makexwalk(file=xwalkpath):
    d = {}
    p = re.compile('[\W_]+')
    with open(file,newline='') as f:
        spam = csv.reader(f,delimiter=',')
        for row in spam:
            d[p.sub('',row[0]+row[1])] = (row[2],row[3],row[4])
    return d
       
#name as full schedule code
def pre_translate(name):
    pattern = re.compile('[\W_]+')
    
    s = pattern.sub(' ',name).split()
    print(s)
    numcount = 0
    function = ''
    schedule = ''
    depo = ''
    pd = 0
    for p,w in enumerate(s):
        if w.isnumeric() and numcount == 0:
            function = w
            numcount += 1
        if w.isnumeric() == False:
            if numcount > 0:
                depo = w
                pd = p
                break
            
    schedule = s[p-1]

    if s[p+1].isnumeric():
        depo += s[p+1]
        if s[p+2].isalpha and len(s[p+2]) < 2:
            depo += s[p+2]

    return (function, schedule, depo)
                
#parse out function, schedule, depo item        
def getcodes(name):

    #find the long schedule code within a name
    pattern = re.compile('\d+-|\d+_')
    s = name.split(' ')
    code = ''
    
    for i in s:
        l = re.search(pattern,i)
        if l != None:
            code = i[l.span()[0]:]

    return pre_translate(code)

#need rework
def translate(name, xwalk):    
    #if len(global xwalk) == 0
        #global xwalk = makexwalk()

    (f,s,d) = getcodes(name)

    try:
        s1,d1,f1 = xwalk[s+d] 
        if s1 == '':
            return('0'+s,'a',f)
        return (s1,d1,f1)    
    except:
        return 'none'

xwalk = makexwalk()

def test():
    print('test')
