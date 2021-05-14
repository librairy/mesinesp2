#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  6 17:36:24 2021

@author: cbadenes
"""
import requests


def get_topics(model,text):
    topics = {}
    topics.setdefault('hierarchy_level_0',[])
    topics.setdefault('hierarchy_level_1',[])
    topics.setdefault('hierarchy_level_2',[])
    increment = int(model)
    port = 8000 + increment
    print("getting topic distribution from medinesp-llda-l"+str(model)+" model")    
    try:
        response = requests.post("http://localhost:"+str(port)+"/classes", json = { 'text':text})
        data = response.json()
                
        for topic in data:
            if (topic['id']== 0):
                topics['hierarchy_level_0'].append(topic['name'])
            elif (topic['id']== 1):
                topics['hierarchy_level_1'].append(topic['name'])    
            else:     
                topics['hierarchy_level_2'].append(topic['name'])
    except:
        print("Error getting topics from ",port)
    return topics

def get_metrics(reference,value):
    reference_list = [str(ref) for ref in reference]
    value_list = [str(val) for val in value]
    tp = 0
    fp = 0
    fn = 0
    for result in value_list:
        if (result in reference_list):
            tp += 1
        else:
            fp += 1
    for data in reference_list:
        if (data not in value_list):
            fn += 1
    precision = 0.0
    if (tp + fp) > 0:
        precision = tp / (tp + fp)
    recall = 0.0
    if (tp + fn) > 0:
        recall = tp / (tp + fn)
    fmeasure = 0.0
    if (precision + recall) > 0:
        fmeasure = 2 * ( (precision * recall) / (precision + recall)  )
    return { 'tp': tp, 'fp': fp, 'fn': fn, 'precision': precision, 'recall': recall, 'fmeasure':fmeasure, 'ref-labels':reference, 'inf-labels':value}

def get_reference_codes(level, article):
    if (level == 0):
        return article['code_levels']
    else:
        return article['codes_level_'+str(level)]

def evaluate(article):

    results = {}
    topic_codes = {'h0':[], 'h1':[], 'h2':[]}
    text = article['bow_t']
    code_levels = [0]
    code_levels.extend(article['code_levels'])
    for level in code_levels:
        if (level > 3):
        # for partial evaluations
            continue
        topics = get_topics(level,text)
        if (level > 0):
            topic_codes['h0'].extend(topics['hierarchy_level_0'])
            topic_codes['h1'].extend(topics['hierarchy_level_0']+topics['hierarchy_level_1'])
            topic_codes['h2'].extend(topics['hierarchy_level_0']+topics['hierarchy_level_1']+topics['hierarchy_level_2'])
        reference_codes = get_reference_codes(level, article)
        
        results['l'+str(level)+'_h0']=get_metrics(reference_codes,topics['hierarchy_level_0'])
        results['l'+str(level)+'_h1']=get_metrics(reference_codes,topics['hierarchy_level_0'] + topics['hierarchy_level_1'])
        results['l'+str(level)+'_h2']=get_metrics(reference_codes,topics['hierarchy_level_0'] + topics['hierarchy_level_1'] + topics['hierarchy_level_2'])
                   
    # evaluate global codes
    reference_codes = article['codes']
        
           
    results['total_h0']=get_metrics(reference_codes,topic_codes['h0'])
    results['total_h1']=get_metrics(reference_codes,topic_codes['h1'])
    results['total_h2']=get_metrics(reference_codes,topic_codes['h2'])     

    response = { 'article_id':article['id'], 'results':results }
    return response
    
    