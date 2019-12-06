import requests

auth = 'Basic bW5ndXllbjpyYW5kb21wYXNzQDEyMw=='


#use for streaming big files
def stream_file(objid,auth=auth):
    url = "https://ecms.epa.gov/dctm-rest/repositories/ecmsrmr65/archived-contents"
    querystring = {"object-id":objid}
    headers = {
        'cache-control': 'no-cache',
        'Authorization': auth 
        }
    
    #local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    
    with requests.get(url, headers=headers, params=querystring, stream=True) as r:
        r.raise_for_status()

        local_filename = r.headers['Content-Disposition'].replace('\"',"")

        p = os.path.join(savepath,str(objid) + ' ' + local_filename)
        with open(p, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    #f.flush()
    f.close()

    #return local_filename

#get only header, wehich contains file size information
def getheader(objid,auth=auth):
    url = "https://ecms.epa.gov/dctm-rest/repositories/ecmsrmr65/archived-contents"
    querystring = {"object-id":objid}

    headers = {
        'cache-control': "no-cache",
        'Authorization': auth
        }


    return requests.head(url, headers=headers, params=querystring, allow_redirects=True)


#direct download    
def getpackage(objid,auth=auth):
    
    url = "https://ecms.epa.gov/dctm-rest/repositories/ecmsrmr65/archived-contents";
    querystring = {"object-id":objid}

    headers = {
        'cache-control': "no-cache",
        'Authorization': auth
        }

    logging.info('Getting objID: ' + objid)

    return requests.request("GET", url, headers=headers, params=querystring)


