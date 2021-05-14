#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 10 11:32:27 2021

@author: cbadenes
"""

import worker.eval as workers
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

    # Create a client instance. The timeout and authentication options are not required.
    categories_as_topics = []
    f = open('../results/topic-models.jsonl', mode='w')
    for port in range(8000,8015):
        level = port % 1000
        print("getting settings from",port,"..")
        settings = get_content("http://localhost:"+str(port)+"/settings")
        if ('stats' in settings):
            print("getting topics from",port,"..")
            topics = get_content("http://localhost:"+str(port)+"/topics")
            for topic in topics:
                topic['level']=level
                categories_as_topics.append(topic)
            num_topics = len(topics)
            stats = settings['stats']
            row = { 'level':level, 'docs':int(stats['corpus']), 'topics':num_topics, 'vocabulary':int(stats['vocabulary']), 'loglikelihood':float(stats['loglikelihood'])}
            f.write(json.dumps(row))
            f.write("\n")
            print(row)
    f.close()

    print("writing categories as topics...")
    f = open('../results/categories_as_topics.jsonl', mode='w')
    for topic_description in categories_as_topics:
        row = {'category':topic_description['name'], 'level':str(topic_description['level']), 'topic':str(topic_description['id']), 'words':topic_description['description']}
        f.write(json.dumps(row))
        f.write("\n")
        print(row)
    f.close()
        

    print("reading development documents..")
    solr = pysolr.Solr('http://librairy.linkeddata.es/data/mesinesp', always_commit=True, timeout=50)
        

    # print report
    f = open('../results/dev-results.jsonl', mode='w')
    print("Number of processors: ", mp.cpu_count())
    pool = mp.Pool(6)
    
    
    sentences = []
    print("reading from solr..")
    counter = 0
    completed = False
    window_size=50
    cursor = "*"

    while (not completed):
        old_counter = counter
        solr_query="scope_s:Development"
        try:
            t = time.time()
            articles = solr.search(q=solr_query,rows=window_size,cursorMark=cursor,sort="id asc")
            cursor = articles.nextCursorMark
            results = pool.map(workers.evaluate,articles.docs)            
            for result in results:
                doc = result['article_id']
                doc_results = result['results']           
                for strategy in doc_results.keys():
                   eval_result = doc_results[strategy]
                   row = { 'doc':doc, 'strategy':strategy, 'tp':eval_result['tp'], 'fp':eval_result['fp'], 'fn':eval_result['fn'], 'precision':eval_result['precision'], 'recall':eval_result['recall'], 'fmeasure':eval_result['fmeasure'], 'ref-labels':eval_result['ref-labels'], 'inf-labels':eval_result['inf-labels']}
                   f.write(json.dumps(row))
                   f.write("\n")
            counter += len(results)
            print(counter,"docs evaluated")
            print('Time to evaluate docs: {} mins'.format(round((time.time() - t) / 60, 2)))
            if (old_counter == counter):
                print("done!")
                break
        except:
            print("Solr query error. Wait for 5secs..")
            time.sleep(5.0)
    f.close()
    
    
    
    
    
    
    
    
    
    
    