import requests
import os


#use for streaming big files
def stream_file(objid,username,password,p=os.getcwd()):
    url = "https://ecms.epa.gov/dctm-rest/repositories/ecmsrmr65/archived-contents"
    querystring = {"object-id":objid}
    headers = {
        'cache-control': 'no-cache'
        }
    
    #local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    
    with requests.get(url, headers=headers, params=querystring, auth=(username,password), stream=True) as r:
        r.raise_for_status()

        local_filename = r.headers['Content-Disposition'].replace('\"',"")

        with open(os.path.join(p,local_filename), 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    #f.flush()
    f.close()

    #return local_filename

#get only header, wehich contains file size information
def getheader(objid,username,password):
    url = "https://ecms.epa.gov/dctm-rest/repositories/ecmsrmr65/archived-contents"
    querystring = {"object-id":objid}

    headers = {
        'cache-control': "no-cache",
        }


    return requests.head(url, headers=headers, params=querystring, auth = (username,password), allow_redirects=True)


#direct download    
def getpackage(objid,username,password):
    
    url = "https://ecms.epa.gov/dctm-rest/repositories/ecmsrmr65/archived-contents";
    querystring = {"object-id":objid}

##    headers = {
##        'cache-control': "no-cache",
##        'Authorization': auth
##        }

    
    return requests.request("GET", url, auth = (username,password), params=querystring)


