#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 10 18:18:23 2021

@author: cbadenes
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 10 13:01:50 2021

@author: cbadenes
"""
import worker.categorize as workers
import pysolr
import multiprocessing as mp
import time


if __name__ == '__main__':
    print("annotating documents..")
    
    solr = pysolr.Solr('http://librairy.linkeddata.es/data/mesinesp', always_commit=True, timeout=50)
    
    print("Number of processors: ", mp.cpu_count())
    pool = mp.Pool(mp.cpu_count())
    
    
    print("reading from solr..")
    counter = 0
    completed = False
    window_size=50
    cursor = "*"
    
    t = time.time()
    while (not completed):
        old_counter = counter        
        try:
            articles = solr.search(q="codes:[* TO *]",rows=window_size,cursorMark=cursor,sort="id asc")
            cursor = articles.nextCursorMark
            results = pool.map(workers.categorize,articles.docs)            
            solr.add(results)
            counter += len(results)
            print(counter,"docs annotated")
            if (old_counter == counter):
                print("done!")
                break
        except:
            print("Solr query error. Wait for 5secs..")
            time.sleep(5.0)
    print('Time to annotate documents: {} mins'.format(round((time.time() - t) / 60, 2)))