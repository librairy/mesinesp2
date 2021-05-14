#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 10 12:16:45 2021

@author: cbadenes
"""

import model.workers as workers
import pysolr
import json
import multiprocessing as mp
import time
import statistics



if __name__ == '__main__':  

    
    solr_query="scope_s:Development"
    solr = pysolr.Solr('http://librairy.linkeddata.es/data/mesinesp', always_commit=True, timeout=50)
        
    print("Number of processors: ", mp.cpu_count())
    pool = mp.Pool(mp.cpu_count())
    
    sentences = []
    print("reading from solr..")
    counter = 0
    completed = False
    window_size=200
    cursor = "*"
    documents = []
    while (not completed):
        old_counter = counter        
        try:
            articles = solr.search(q=solr_query,rows=window_size,cursorMark=cursor,sort="id asc")
            cursor = articles.nextCursorMark
            results = pool.starmap(workers.inference,[(article['id'],article['abstract_t']) for article in articles.docs] )            
            documents.extend(results)
            counter += len(results)
            print(counter,"docs evaluated")
            if (old_counter == counter):
                print("done!")
                break
        except:
            print("Solr query error. Wait for 5secs..")
            time.sleep(5.0)
    
    
    with open('baseline-llda-l0.json', 'w') as outfile:
        json.dump({'documents':[doc['result0'] for doc in documents]}, outfile)
    with open('baseline-llda-l1.json', 'w') as outfile:
        json.dump({'documents':[doc['result1'] for doc in documents]}, outfile)
    with open('baseline-llda-l2.json', 'w') as outfile:
        json.dump({'documents':[doc['result2'] for doc in documents]}, outfile)
    
    pool.close()