#!/usr/bin/env python3
# 
import time
import json
import http.client
from concurrent.futures import ThreadPoolExecutor# creates a list of values as long as the number of things we want# in parallel so we could associate an ID to each
 
parallel = 5
runs=[value for value in range(parallel)]
 
def getpage(id): 
    try: 
        host = "07z3tk03ye.execute-api.us-east-1.amazonaws.com" 
        c = http.client.HTTPSConnection(host) 
        data = {
        "D":2,
        "Q":1000,
        "S":100000
        } 
        c.request("POST", "/default/course_work", json.dumps(data)) 
        response = c.getresponse() 
        data = response.read().decode('utf-8') 
        print( data, " from Thread", id ) 
    except IOError: 
        print( 'Failed to open ', host ) # Is the Lambda address correct? 
        print(data+" from "+str(id)) # May expose threads as completing in a different order 
        return "page "+str(id)
 
def getpages(): 
    with ThreadPoolExecutor() as executor: 
        results=executor.map(getpage, runs) 
    return results
 
if __name__ == '__main__':
    start = time.time() 
    results = getpages() 
    
for result in results: # uncomment to see results in ID order # 
     print(result)
 
print( "Elapsed Time: ", time.time() - start)





# https://07z3tk03ye.execute-api.us-east-1.amazonaws.com/default/course_work
# curl -d '{"Q":1000,"D":5,"S":100000}' https://07z3tk03ye.execute-api.us-east-1.amazonaws.com/default/course_work