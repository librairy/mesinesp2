#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 10 18:31:19 2021

@author: cbadenes
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  6 17:36:24 2021

@author: cbadenes
"""
import networkx as nx
import obonet
import re


# Read the taxrank ontology
url = '/Users/cbadenes/Dropbox/Trabajo/Carlos/OEG/Projects/MESINESP/data/DeCS2020.obo'
graph = obonet.read_obo(url)

print("reading graph from obo file..")
print(nx.info(graph))


def get_name(id):
    return  re.search("\"(.*)\"", id).group(1)

    
nodes = list(graph.nodes(data=True))
root_node = nodes[0][0]

print("build hierarchy..")
hierarchy = {}
counter = 0
pending_nodes = []
for node in nodes:
    id = get_name(node[0])
    deep = nx.shortest_path_length(graph, source=node[0], target=root_node)
    name = node[1]['name']
    parents = []
    if ('is_a' in node[1]):
        parents = node[1]['is_a']
    hierarchy[id]={ 'name': name, 'deep': deep, 'parents': [get_name(parent) for parent in parents]}
    counter += 1
    if (counter % 100 == 0):
        print(counter,"nodes loaded")   
    
    
def categorize(article):
    for i in range(15):
        label = "codes_level_"+str(i)
        if (label in article):
            article.pop(label)
    code_levels = []
    for code in article['codes']:
        hierarchy_code = hierarchy[code]
        deep = hierarchy_code['deep']
        code_label = 'codes_level_'+str(deep)
        if (code_label not in article):
            article[code_label]=[code]
            code_levels.append(str(deep))
        else:
            article[code_label].append(code)
    article['code_levels']=code_levels
    return article
    
    
    
    
    
    