from flask import Flask, render_template,redirect,url_for,request,jsonify
import json,random
app=Flask(__name__)

import math
import random
import time
import json
import http.client
import statistics
from concurrent.futures import ThreadPoolExecutor# creates a list of values as long as the number of things we want# in parallel so we could associate an ID to each
results=[]
avg= None
values_estimates=[]
estimates_pi=[]
flat_list1=[]
# calling calculation functions

def calculation(s):
    val=[]
    print("cal_reached",s)
    for i in s:
        val.append(i['values'])
        # resource_id.append(i['Resource_id'])
        # incircle_values.append(i['incircle_values'])
        # number_shots.append(i['number_shots'])
    #print(val)     
    #print(resource_id) 
    #print(incircle_values) 
    #print(number_shots)
    #val = map(float, val) 
    #avg=statistics.mean(val) 
    print("Value******",val)
    return val


    

def getpage(id,matching,shots,rate):
    try: 
        host = "07z3tk03ye.execute-api.us-east-1.amazonaws.com" 
        c = http.client.HTTPSConnection(host) 
        data = {
        "rid":id,
        "D":matching,
        "Q":rate,
        "S":shots
        } 
        c.request("POST", "/default/course_work", json.dumps(data)) 
        response = c.getresponse() 
        print("AWS response",response)
        data = json.loads(response.read().decode('utf-8'))
        #data.update({"Resource_id":id})
        print( data)
        return data 
    except IOError: 
        print( 'Failed to open ', host ) # Is the Lambda address correct? 
        print(data+" from "+str(id)) # May expose threads as completing in a different order 
        return "page "+str(id)
 
def getpages(matching,shots,rate,runs): 
    with ThreadPoolExecutor() as executor: 
        #results=executor.map(getpage, runs)
        
        
        for i in runs:
            data=getpage(i,int(matching),int(shots),int(rate))
            print("getpage_data",data)
            results.append(data)
    return results
def do_something(matching,shots,rate,no_resource):
    parallel = no_resource
    runs=[value for value in range(parallel)]
    print("there")
    getpages(matching,shots,rate,runs)
    
 
    #if __name__ == '__main__':
        # start = time.time() 
        # results = getpages() 
    
    for result in results: # uncomment to see results in ID order # 
        print(result)
 
    # print( "Elapsed Time: ", time.time() - start)
    return results
 

@app.route('/',methods=['GET','POST'])
def home():
    if request.method == 'POST':
        resource_type = request.form['Function']
        print(resource_type)
        no_resource= request.form['Services']
        print(no_resource)
        return redirect(url_for('ranjeet',resource_type=resource_type,no_resource=no_resource))
    else:
        return render_template('index.html') 
    
@app.route('/<resource_type>/<no_resource>',methods=['GET','POST'])
def ranjeet(resource_type,no_resource):
    if resource_type=="EC2":
        print("Please enter labda and go back")
    else:
        print("here",resource_type,no_resource)
        if request.method == 'POST':
            matching = request.form['Matching']
            print(matching)
            shots= request.form['shots']
            shots=int(shots)/int(no_resource)
            print(shots)
            rate= request.form['rate']
            print(rate)
            # start = time.time() 
            
            s=do_something(matching,shots,rate,int(no_resource))
            print("Ranjeet_s",s)
            pi_values=calculation(s)
            
            print("pi average value",pi_values)
            for i in pi_values:
               values_estimates.append(json.loads(i))
            print("list of pi values",values_estimates)
            flat = [item for sublist in values_estimates for item in sublist]
            for i in flat:  
                flat_list1.append(i[0]/i[1]*4)
            flat_list=[]
            for i in flat_list1:
                if i!=0.0:
                    flat_list.append(i)
            print("flat_list******",flat_list)
            actual_pi=math.pi
            print('ap',actual_pi)
            #return redirect(url_for('graph',resource_type=resource_type,no_resource=no_resource,matching=matching,shots=shots,rate=rate))
            return render_template('graph.html',shots=shots,rate=rate,s=s,actual_pi = actual_pi,matching=matching,flat_list=flat_list)
        else:
            return render_template('ranjeet.html') 

@app.route('/graph')
def graph():
    return render_template('graph.html') 
@app.route('/join', methods=['GET','POST'])
def my_form_post():
    text1 = request.form['text1']
    
    #word = request.    gs.get('text1')
    combine = do_something(text1)
    
    #console.log(combine)
    result = {
        "output": combine
    }
    result = {str(key): value for key, value in result.items()}
    print(result)
    return jsonify(result=result)

if __name__ == '__main__':
    app.run(debug=True)


    
