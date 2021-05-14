#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 12 18:46:37 2021

@author: cbadenes
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 10 11:32:27 2021

@author: cbadenes
"""

import worker.test as worker
import pysolr
import multiprocessing as mp
import time
import json
import requests

def get_content(url):
    content = {}
    try:
        response = requests.get(url)
        content = response.json()
    except:
        print("Error getting from url: ",url)
    return content

if __name__ == '__main__':  

    
    print("reading test documents..")
    solr = pysolr.Solr('http://librairy.linkeddata.es/data/mesinesp', always_commit=True, timeout=50)
        

    # print report
    f = open('../results/test-results.json', mode='w')
    print("Number of processors: ", mp.cpu_count())
    pool = mp.Pool(6)
    
    
    print("reading from solr..")
    counter = 0
    completed = False
    window_size=200
    cursor = "*"
    level0_result = {}
    level0_result.setdefault('documents',[])
    level1_result = {}
    level1_result.setdefault('documents',[])
    level2_result = {}
    level2_result.setdefault('documents',[])
    
    while (not completed):
        old_counter = counter
        solr_query="scope_s:Test"
        try:
            articles = solr.search(q=solr_query,rows=window_size,cursorMark=cursor,sort="id asc")
            cursor = articles.nextCursorMark
            results = pool.map(workers.test,articles.docs)            
            for result in results:
                doc0 = { 'id':result['id'], 'labels':result['labels0']}
                level0_result.append(doc0)
                
                doc1 = { 'id':result['id'], 'labels':result['labels1']}
                level1_result.append(doc1)
                
                doc2 = { 'id':result['id'], 'labels':result['labels2']}
                level2_result.append(doc2)
            counter += len(results)
            print(counter,"docs evaluated")
            if (old_counter == counter):
                print("done!")
                break
        except:
            print("Solr query error. Wait for 5secs..")
            time.sleep(5.0)
    print("writing json files...")
    with open("../results/test_level0.json", "w") as write_file:
        json.dump(level0_result, write_file)
    with open("../results/test_level1.json", "w") as write_file:
        json.dump(level1_result, write_file)
    with open("../results/test_level2.json", "w") as write_file:
        json.dump(level2_result, write_file)
    
    
    
    
    
    
    
    
    
    
    