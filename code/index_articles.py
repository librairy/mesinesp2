#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  6 14:57:08 2021

@author: cbadenes
"""
import worker.index as workers
import pysolr
import json
import multiprocessing as mp


if __name__ == '__main__':  

    # Create a client instance. The timeout and authentication options are not required.
    solr = pysolr.Solr('http://librairy.linkeddata.es/data/mesinesp', always_commit=True, timeout=50)
        
    
    directory   = "/Users/cbadenes/Dropbox/Trabajo/Carlos/OEG/Projects/MESINESP/data"
    #track       = 'Subtrack2-Clinical_Trials'
    track       = 'Subtrack3-Patents'
    identifier  = 'track3'
    #files       = {'Development': ('development_set_subtrack2.json','entities_subtrack2_development.json'),
    #         'Test': ('test_set_subtrack2.json','entities_subtrack2_test.json'),
    #         'Train': ('training_set_subtrack2.json','entities_subtrack2_train.json')}
    files       = {'Development': ('development_set_subtrack3.json','entities_subtrack3_development.json'),
             'Test': ('test_set_subtrack3.json','entities_subtrack3_test.json')}
    
    
    
    for scope in files.keys():
        print("loading scope:",scope)
        data_file = files[scope][0]
        with open(directory + "/" + track + "/" + scope + "/" + data_file) as json_file:
            data = json.load(json_file)
    
        
        
        print("loading additional data file..")
        additional_file = files[scope][1]
        entities = {}
        with open(directory + "/Additional data/" + track + "/" + additional_file) as json_file:
            for article in json.load(json_file)['articles']:
                article_entities = {}
                article_entities['diseases']= article['diseases']
                article_entities['medications']= article['medications']
                article_entities['procedures']= article['procedures']
                article_entities['symptoms']= article['symptoms']
                entities[article['id']]=article_entities
    
    
        #article = data['articles'][1]
        #doc = workers.create_document(article, entities[article['id']],scope,True)
        #print(doc)
    
        print("Number of processors: ", mp.cpu_count())
        pool = mp.Pool(mp.cpu_count())
        
        max_length = len(data['articles'])
        increment = 100
        min_idx = 0
        max_idx = increment
        while(min_idx<max_length):
            print("indexing",max_idx,"documents..")
            #results = pool.map(workers.create_document,[article for article in data['articles'][min_idx:max_idx]] )
            results = pool.starmap(workers.create_document,[(article,identifier,entities[article['id']],scope,True) for article in data['articles'][min_idx:max_idx]] )
            min_idx = max_idx
            max_idx = min_idx + increment
            solr.add(results)
        
        pool.close()
    
    
    
    
    
    
    
    
    
    