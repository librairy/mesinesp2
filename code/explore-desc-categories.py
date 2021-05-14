#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 13 13:21:42 2021

@author: cbadenes
"""
import worker.eval as workers_eval
import worker.index as workers_index
import pysolr

# Create a client instance. The timeout and authentication options are not required.
solr = pysolr.Solr('http://librairy.linkeddata.es/data/decs', always_commit=True, timeout=50)


def get_category(id):
    result = solr.search("id:"+id)
    return result.docs[0]
    

category = get_category("D009042")
print("Id:",category['id'])
name = category['name_s']
print("Name:",name)
text = name
if 'definition_s' in category:
    text += " " + category['definition_s']
#if 'synonyms' in category:
#    for synonym in category['synonyms']:
#        text += " " + synonym    
# transform to bow
tokens = workers_index.get_tokens(text)
print(tokens)
bow = workers_index.get_bow(tokens)
print("BoW:",bow)
# get topics
topics = workers_eval.get_topics(category['deep_i'], bow)
print("Topics:",topics)    

for i in range(3):
    print("Level"+str(i)+":")
    for topic in topics['hierarchy_level_'+str(i)]:
        print(get_category(topic)) 

