#Generate csv of object id and schedule id, of all items within a schedule  

import requests
import os
import csv
import json
import time

fpsource = ''
objid= r''
auth = 'Basic bW5ndXllbjpyYW5kb21wYXNzQDEyMw=='

#Retrieve json list of object id for a giving fp

def getlist(fp,page):
    
    url = "https://ecms.epa.gov/dctm-rest/repositories/ecmsrmr65"

    querystring = {"dql" : f"select r_object_id,object_name from erma_doc where folder ('/erma/EPA_File_Plan/{fp}')",
                   "items-per-page" : 1000,
                   "page": page}
                   
    #querystring = {"dql" : "select r_object_id,object_name from erma_doc where folder ('/erma/EPA_File_Plan/304-107_105_a(2)')",
                   #"items-per-page" : 1000,
                   #"page": page}

    headers = {
        'Authorization': auth
        }
    #return querystring
    return requests.request("GET", url, headers=headers, params=querystring)

def clist(response):
    w=[]
    j = json.loads(r.text)
    try:
        for i in j['entries']:
            if i['content']['properties']['r_object_id'] not in w:
                w.append(i['content']['properties']['r_object_id'])

        return w
    except KeyError:
        return('None')


        
#increment page until response returns 'none'
if __name__ == "__main__":

    fpl = open(fpsource,'rt')
    fpq = []

    while True:
        item = fpl.readline()
        if item == '':
            break
        fpq.append(item.strip())
        
    cl = 'Start'
    c = []
    
    cfile = open('objid.csv', 'w', newline = '')
    sp = csv.writer(cfile)


    for i in fpq:
        page = 1
        while True:
            r = getlist(i,page)
            ct = clist(r)
            if ct == 'None':
                break
            for e in ct:
                sp.writerow([e,i])
            page += 1
            

    cfile.close()

    print('Completed')    

        
