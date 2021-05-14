#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  9 08:56:19 2021

@author: cbadenes
"""

import multiprocessing

import gensim

from gensim.models import Word2Vec

import pysolr

import time


# Create a client instance. The timeout and authentication options are not required.
solr = pysolr.Solr('http://librairy.linkeddata.es/data/mesinesp', always_commit=True, timeout=50)


sentences = []
print("reading from solr..")
counter = 0
completed = False
window_size=200
cursor = "*"
while (not completed):
    old_counter = counter
    solr_query="size_i:[100 TO *] AND scope_s:Train"
    try:
        articles = solr.search(q=solr_query,rows=window_size,cursorMark=cursor,sort="id asc")
        cursor = articles.nextCursorMark
        list_articles = articles.docs
        for article in  list_articles:
            sentences.append(article['tokens'])
        counter += len(list_articles)
        print(counter,"docs read")
        if (old_counter == counter):
            print("done!")
            break
    except:
        print("Solr query error. Wait for 5secs..")
        time.sleep(5.0)


print(counter,"documents read")

print("ready to train w2v model..")
cores = multiprocessing.cpu_count() 

w2v_model = Word2Vec(min_count=10,
                     window=4,
                     vector_size=300,
                     sample=6e-5, 
                     alpha=0.03, 
                     min_alpha=0.0007, 
                     negative=20,
                     workers=cores-1)


t = time.time()

w2v_model.build_vocab(sentences, progress_per=10000)

print('Time to build vocab: {} mins'.format(round((time.time() - t) / 60, 2)))


t = time.time()

w2v_model.train(sentences, total_examples=w2v_model.corpus_count, epochs=30, report_delay=1)

print('Time to train the model: {} mins'.format(round((time.time() - t) / 60, 2)))

w2v_model.init_sims(replace=True)


w2v_model.save("../models/word2vec.model")