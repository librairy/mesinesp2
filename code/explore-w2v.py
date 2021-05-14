#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 13 11:18:22 2021

@author: cbadenes
"""
import worker.eval as workers
from gensim.models import Word2Vec
import pysolr



#########################################################################################################
## {"doc": "ibc-FGT-2201", "strategy": "l3_h0", "ref-labels": ["D009042"], "inf-labels": ["D061485"]}
#########################################################################################################
doc_id = "ibc-FGT-2201"

model_level = 3

#########################################################################################################
#########################################################################################################

# Create a client instance. The timeout and authentication options are not required.
solr = pysolr.Solr('http://librairy.linkeddata.es/data/mesinesp', always_commit=True, timeout=50)


model = Word2Vec.load("../models/word2vec.model")

articles = solr.search("id:"+doc_id)

article = articles.docs[0]

bow = article['bow_t']

for term in bow.split(" "):
    print(">>>>",term)
    if ("=" not in term):
        continue
    word = term.split("=")[0]
    freq = term.split("=")[1]
        
    try:
        sims = model.wv.most_similar(word, topn=1)
        for sim in sims:
            print(sim)
            sim_word = sim[0]
            new_term = sim_word + "=" + freq
            bow += new_term + " "
            print("added",new_term)
    except:
        print("similar words not found for",word)

topics = workers.get_topics(model_level,bow)

print(topics)