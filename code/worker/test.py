#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 12 18:51:11 2021

@author: cbadenes
"""

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


def get_labels(article):

    response = { 'id':article['id'] }
    response.setdefault('labels0',[])
    response.setdefault('labels1',[])
    response.setdefault('labels2',[])

    text = article['bow_t']
    # Test documents
    levels_per_hierarchy = get_topics(0,text)
    for strategy in range(3):
        for level in levels_per_hierarchy['hierarchy_level_'+str(strategy)]:
            topics = get_topics(level,text)
            if (strategy == 0):
                response['labels0'].extend(topics['hierarchy_level_0'])
            elif (strategy == 1):
                response['labels1'].extend(topics['hierarchy_level_0']+topics['hierarchy_level_1'])
            else:
                response['labels2'].extend(topics['hierarchy_level_0']+topics['hierarchy_level_1']+topics['hierarchy_level_2'])

    return response
    
    